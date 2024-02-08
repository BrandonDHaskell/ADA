import os
import re
import logging
import time
import isodate
from dotenv import load_dotenv
from datetime import datetime, timedelta
from dateutil import parser, rrule
from zoneinfo import ZoneInfo
from threading import Thread, Event

import RPi.GPIO as GPIO
from src.utils.logging_utils import setup_logging
from src.database.implementations.json_database import JsonDatabase
from src.hardware.implementations.mfrc522_reader import MFRC522Reader
from src.hardware.implementations.continuous_switch_monitor import ContinuousSwitchMonitor
from src.hardware.implementations.pi_gpio_switch_reader import PiGPIOSwitchReader
from src.hardware.implementations.pi_gpio_switch_operator import PiGPIOSwitchOperator
from src.hardware.implementations.continuous_mfrc522_scanner import RFIDContinuousMonitor
from src.utils.threading_shared_variable import SharedVariable
from src.schemas.member_schema import member_schema

# Configure basic logging for now
# TODO - make this an app configuration
setup_logging(logging.DEBUG)
logger = logging.getLogger('ADA')

if load_dotenv():
    logger.info("Environment variables loaded")
else:
    logger.info("No environment variables passed, loading defaults")

class AddMemberModeManager:
    def __init__(self):
        self.thread_stop_event = Event()
        self.thread = None

    def start_add_member_mode(self, db, rfid_monitor_shared_var, get_temp_access_interval):
        if not self.is_active():
            self.thread_stop_event.clear()
            self.thread = Thread(target=self.handle_active_mode, args=(db, rfid_monitor_shared_var, get_temp_access_interval, self.thread_stop_event))
            self.thread.start()

    def stop_add_member_mode(self):
        if self.is_active():
            self.thread_stop_event.set()
            self.thread.join()
            self.thread = None

    def is_active(self):
        return self.thread is not None and self.thread.is_alive()
    
    @staticmethod
    def handle_active_mode(db, rfid_monitor_shared_var, get_temp_access_interval, stop_event):
        guest_member_info = {}
        sponsor_member_info = {}
        sponsor_obf_id = None
        guest_obf_id = None
        is_valid_sponsor = False
        continue_loop = True

        # Loop until one of these occurs:
            #   + timeout
            #   + add/update guest to DB
            #   + sponsor not authorized
        while not stop_event.is_set():
            """
            Loop until sponsor ID is scanned and guest ID is scanned
            Then determine if sponsor can sponsor the guest
            """
            # Scan for and RFID
            obf_id = rfid_monitor_shared_var.get()

            # Get sponsor ID first and run validation checks
            if obf_id is not None and sponsor_obf_id is None:

                logger.info(f"Sponsor RFID scanned: {sponsor_obf_id}")
                sponsor_member_info = db.get_member({"obf_rfid": sponsor_obf_id})

                # Check if sponsor is in DB and is a valid sponsor
                if sponsor_member_info is not None and is_valid_sponsor(sponsor_member_info):
                    is_valid_sponsor = True
                    # TODO - notify user
                    logger.info(f"Sponsor is authorized")
                else:
                    logger.info("Sponsor not authorized")
                    continue_loop = False
                    # stop thread

            # Get guest ID and determine if adding or updating
            if obf_id is not None and sponsor_obf_id is not None and guest_obf_id is None:
                
                # Scan guest ID
                guest_obf_id = rfid_monitor_shared_var.get()
                logger.info(f"Guest RFID scanned: {guest_obf_id}")

                # if guest_obf_id was scanned, determine if guest is updating or creating a record
                if is_valid_sponsor and guest_obf_id is not None:

                    # Assume guest is new and check if renewing temp access
                    guest_is_new = True

                    # Check if Guest exists in DB
                    guest_member_info = db.get_member({"obf_rfid": guest_obf_id})
                    if guest_member_info is not None:
                        guest_is_new = False
                        logger.info(f"Renewing guest temp access: {guest_obf_id}")
                    else:
                        guest_member_info = {
                            "obf_rfid": guest_obf_id,
                            "member_level": "guest",
                            "membership_status": "active",
                            "access_interval": get_temp_access_interval(),
                            "member_sponsor": sponsor_obf_id,
                            "created": "",
                            "last_updated": ""
                        }
                        db.add_member(guest_member_info)
                        logger.info(f"Guest added: {guest_member_info}")

            if continue_loop:
                stop_event.wait(timeout=1)
            else:
                stop_event.clear()

# Check to confirm member data format follows ADA member_schema
def _is_valid_member_data(member_data):
    for key, expected_type in member_schema.items():
        if key not in member_data or not isinstance(member_data[key], expected_type):
            raise ValueError(f"Invalid member data for {key}")
    return True

# Check membership status
def _is_member_status_active(member_data):
    if member_data["membership_status"] == "active":
        return True
    return False

# Check membership access interval
def _is_within_access_interval(interval_str):
    try:
        # Extract the repetition count, start date-time, and duration from the interval string
        match = re.match(r"R(\d*)/(.*?)/(P.*)", interval_str)
        if not match:
            raise ValueError("Invalid interval string format")

        repeat_count, start_str, duration_str = match.groups()

        # If repeat_count is empty, it means infinite repetitions; otherwise, convert to int
        repeat_count = int(repeat_count) if repeat_count else None

        # Parse the start time in the scanner's local timezone and duration
        local_tz = ZoneInfo(os.getenv("SCANNER_TIME_ZONE", "UTC"))
        start_time_local = parser.isoparse(start_str).replace(tzinfo=local_tz)

        # Convert start time from local to UTC (system time)
        start_time_utc = start_time_local.astimezone(ZoneInfo("UTC"))
        duration = _parse_duration(duration_str)

        # Create rule for repeating intervals
        rule = rrule.rrule(rrule.DAILY, interval=1, dtstart=start_time_utc, count=repeat_count)

        # Get current UTC time
        current_time_utc = datetime.now(ZoneInfo("UTC"))

        # Find the current interval in UTC
        current_interval_start = rule.before(current_time_utc, inc=True)
        
        # If interval is in the future, value will be none
        if current_interval_start is None:
            return False
        
        current_interval_end = current_interval_start + duration
        
        # Check if current UTC time is within the interval
        return current_interval_start <= current_time_utc <= current_interval_end
    except Exception as e:
        logger.error(f"Error parsing interval: {e}")
        return False

# Helper function for access interval resolving
def _parse_duration(duration_str):
    # Parse the ISO 8601 duration string
    return isodate.parse_duration(duration_str)


def is_member_access_authorized(member_data):
    # Confirm ADA schemas are being followed
    if not _is_valid_member_data(member_data):
        logger.error("Member Data not in expected format")
        return False
    
    # If member is not active they are not authorized
    if not _is_member_status_active(member_data):
        return False
    
    # If level is 'member' or 'admin' they have 24/7 access
    if member_data["member_level"] == "member" or member_data["member_level"] == "admin":
        return True
    
    # If level is 'guest' or 'philanthropist' they have limited access and we need to validate
    # the scan time is within that interval of limited access
    elif member_data["member_level"] == "guest" or member_data["member_level"] == "philanthropist":
        
        # If current scan time is within the temp access interval, grant access
        if _is_within_access_interval(member_data["access_interval"]):
            return True
        return False
    
    # If an unknown member_level is provided report error
    else:
        logger.error("Member level provided does not exist")
    
    return False

# 
def _sponsorship_is_authorized(member_data):
    pass

def get_temp_access_interval():
    """
    Generates a repeating temporary access interval string based on current UTC date and environment variables.

    Returns:
    str: A repeating interval string in ISO 8601 format.
    """
    # Read values from environment variables
    start_time_str = os.getenv("TEMP_ACCESS_DAY_START_TIME", "12:00")
    duration_hours = int(os.getenv("TEMP_ACCESS_DURATION_HOURS", "8"))
    repeat_days = int(os.getenv("TEMP_ACCESS_DAYS", "1"))

    # Current UTC date and time
    current_utc = datetime.now(ZoneInfo("Etc/UTC"))

    # Parse start hour and minute
    start_hour, start_minute = map(int, start_time_str.split(':'))

    # Start of the access interval (today at the specified start_hour and start_minute, in UTC)
    start_of_interval = current_utc.replace(hour=start_hour, minute=start_minute, second=0, microsecond=0)

    # Adjust if the start time has already passed for today
    if start_of_interval < current_utc:
        start_of_interval += timedelta(days=1)

    # Duration of the access interval
    duration = timedelta(hours=duration_hours)

    # Format the interval in ISO 8601 repeating interval format
    interval_str = f"R{repeat_days}/{start_of_interval.isoformat()}/PT{duration.seconds // 3600}H"
    return interval_str

# Helper method that generates a python boolean value for .env inputs
def str_to_bool(s):
    return s.lower() in ("true", "t", "1", "yes")

def main():
    add_member_mode_manager = AddMemberModeManager()

    GPIO.setmode(GPIO.BCM)
    
    """
    Initialize integrated components and hardware
    """

    # Initialize database
    db = JsonDatabase({
        "name": os.getenv("JSON_DB_NAME", "default_JsonDB"),
        "connection_info": os.getenv("JSON_DB_CONNECTION_INFO", "default_json_database/db.json")
    })

    # Initialize a ModeSwitch
    mode_switch = PiGPIOSwitchReader({
        "name": os.getenv("MODE_SWITCH_NAME", "default_ModeSwitch"),
        "pin_number": int(os.getenv("MODE_SWITCH_PIN_NUMBER", 18)),
        "normally_open": str_to_bool(os.getenv("MODE_SWITCH_NORMALLY_OPEN", "True")),
        "common_to_ground": str_to_bool(os.getenv("MODE_SWITCH_COMMON_TO_GROUND", "True"))
    })

    # Initialize a DoorReedSwitch
    door_reed_switch = PiGPIOSwitchReader({
        "name": os.getenv("REED_SWITCH_NAME", "default_ReedSwitch"),
        "pin_number": int(os.getenv("REED_SWITCH_PIN_NUMBER", 4)),
        "normally_open": str_to_bool(os.getenv("REED_SWITCH_NORMALLY_OPEN", "True")),
        "common_to_ground": str_to_bool(os.getenv("REED_SWITCH_COMMON_TO_GROUND", "True")),
    })

    # Initialize a DoorLatch
    door_latch = PiGPIOSwitchOperator({
        "name": os.getenv("DOOR_SWITCH_NAME", "default_DoorLatch"), 
        "pin_number": int(os.getenv("DOOR_SWITCH_PIN_NUMBER", 21))
    })

    # Initialize an MFRC522Reader
    rfid_reader = MFRC522Reader({
        "name": os.getenv("RFID_READER_NAME", "default_RfidReader")
    })

    
    """
    Initialize hardware state monitors
    """

    # Initialize a ContinuousSwitchMonitor for the ModeSwitch
    mode_monitor_shared_var = SharedVariable() # For switch state access in main
    mode_monitor = ContinuousSwitchMonitor({
    "name": os.getenv("MODE_MONITOR_NAME", "default_ModeMonitor"),
    "monitoring_interval": float(os.getenv("MODE_MONITOR_INTERVAL", 1)),
    "threading_shared_var": mode_monitor_shared_var,
    "switch_reader": mode_switch
    })

    # Initialize a ContinuousSwitchMonitor for the DoorReedSwitch
    door_monitor_shared_var = SharedVariable() # For switch state access in main
    door_monitor = ContinuousSwitchMonitor({
    "name": os.getenv("DOOR_MONITOR_NAME", "default_DoorMonitor"),
    "monitoring_interval": float(os.getenv("DOOR_MONITOR_INTERVAL", 30)),
    "threading_shared_var": door_monitor_shared_var,
    "switch_reader": door_reed_switch
    })

    # Initialize a ContinuousSwitchMonitor for the MFRC522Reader
    rfid_monitor_shared_var = SharedVariable() # For switch state access in main
    rfid_monitor = RFIDContinuousMonitor({
    "name": os.getenv("RFID_MONITOR_NAME", "default_RfidMonitor"),
    "monitoring_interval": float(os.getenv("RFID_MONITOR_INTERVAL", 5)),
    "threading_shared_var": rfid_monitor_shared_var,
    "mfrc522_reader": rfid_reader
    })

    # Start the monitoring threads
    door_monitor.start_monitoring()
    # mode_monitor.start_monitoring()
    rfid_monitor.start_monitoring()
    

    try:
        logger.info("Starting ADA")
        while True:
            # Set the mode state fron the mode_monitor_shared_var
            mode_state = mode_switch.get_status().lower()

            # If 'inactive', then run standard routine logic
            if mode_state == "inactive":

                # Check for updates to rfid_monitor_shared_var
                obf_id = rfid_monitor_shared_var.get()
                if obf_id is not None:
                    logger.info(f"RFID scanned: {obf_id}")

                    # Validate against database
                    member_info = db.get_member({"obf_rfid": obf_id})
                    if member_info:
                        if is_member_access_authorized(member_info):
                            logger.info("Access authorized")
                            # Unlock the door
                            door_latch.set_status("active")
                            logger.info("Door unlocked")

                            # Keep the door unlocked for 7 seconds
                            time.sleep(7)

                            # Lock the door again
                            door_latch.set_status("inactive")
                            logger.info("Door locked")
                        else:
                            logger.info("Access not authorized")    
                    else:
                        logger.info("Access not authorized")

                    # Reset variable for next iteration
                    rfid_monitor_shared_var.reset()

            # If 'active', then run add member logic
            elif mode_state == "active":
                if not add_member_mode_manager.is_active():
                    # Start active mode thread if not already running
                    add_member_mode_manager.start_add_member_mode(db, rfid_monitor_shared_var, get_temp_access_interval)
                    logger.info("Add Member Mode processing started")
            elif mode_state == "inactive":
                if add_member_mode_manager.is_active():
                    # Stop the active mode thread if it's running and we're no longer in active mode
                    add_member_mode_manager.stop_add_member_mode()
                    logger.info("Add Member Mode processing stopped")
            else:
                if mode_state is not None:
                    logger.warning(f"Unknown mode state")

            # Check for updates in door_monitor_shared_var
            door_state = door_monitor_shared_var.get()
            if door_state is not None:
                logger.info(f"Door State Updated: {door_state}")
                # Add notification logic here
            door_monitor_shared_var.reset()  # Reset after logging the update

            # Reset mode_switch for next iteration
            mode_monitor_shared_var.reset()
            time.sleep(0.5)
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt detected. Shutting down ADA...")

    finally:
        # Stop procesing Add Memebers
        if add_member_mode_manager.is_active():
            logger.info("Stopping Add Member Mode processing...")
            add_member_mode_manager.stop_add_member_mode()

        # Stopping the monitors before exiting (cleanup)
        rfid_monitor.stop_monitoring()
        door_monitor.stop_monitoring()
        # mode_monitor.stop_monitoring()
        GPIO.cleanup()
        logger.info("ADA shutdown completed.")


if __name__ == "__main__":
    main()