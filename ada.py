import os
import logging
import time
import RPi.GPIO as GPIO
from dotenv import load_dotenv

from src.utils.logging_utils import setup_logging
from src.database.implementations.json_database import JsonDatabase
from src.hardware.implementations.mfrc522_reader import MFRC522Reader
from src.hardware.implementations.continuous_switch_monitor import ContinuousSwitchMonitor
from src.hardware.implementations.pi_gpio_switch_reader import PiGPIOSwitchReader
from src.hardware.implementations.pi_gpio_switch_operator import PiGPIOSwitchOperator
from src.hardware.implementations.continuous_mfrc522_scanner import RFIDContinuousMonitor
from src.utils.threading_shared_variable import SharedVariable

# Configure basic logging for now
# TODO - make this an app configuration
setup_logging(logging.DEBUG)
logger = logging.getLogger('ADA')

if load_dotenv():
    logger.info("Environment variables loaded")
else:
    logger.info("No environment variables passed, loading defaults")


# Help method that generates a boolean value for .env
def str_to_bool(s):
    return s.lower() in ("true", "t", "1", "yes")

def main():
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
    "threading_shared_var": SharedVariable(),
    "switch_reader": mode_switch
    })

    # Initialize a ContinuousSwitchMonitor for the DoorReedSwitch
    door_monitor_shared_var = SharedVariable() # For switch state access in main
    door_monitor = ContinuousSwitchMonitor({
    "name": os.getenv("DOOR_MONITOR_NAME", "default_DoorMonitor"),
    "monitoring_interval": float(os.getenv("DOOR_MONITOR_INTERVAL", 30)),
    "threading_shared_var": SharedVariable(),
    "switch_reader": door_reed_switch
    })

    # Initialize a ContinuousSwitchMonitor for the MFRC522Reader
    rfid_monitor_shared_var = SharedVariable() # For switch state access in main
    rfid_monitor = RFIDContinuousMonitor({
    "name": os.getenv("RFID_MONITOR_NAME", "default_RfidMonitor"),
    "monitoring_interval": float(os.getenv("RFID_MONITOR_INTERVAL", 5)),
    "threading_shared_var": SharedVariable(),
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
            mode_state = mode_switch.get_status()
            logger.info(f"Current mode state: {mode_state}")

            # If 'inactive', then run standard routine logic
            if mode_state == "inactive":

                # Check for updates in rfid_monitor_shared_var
                obf_id = rfid_monitor_shared_var.get()
                if obf_id is not None:
                    logger.info(f"RFID State Updated: {obf_id}")

                    # Validate against database
                    is_member = db.get_member({"obf_rfid": obf_id})
                    if is_member:
                        logger.info("Access granted")
                        # Unlock the door
                        door_latch.set_status("active")
                        logger.info("Door unlocked")

                        # Keep the door unlocked for 7 seconds
                        time.sleep(7)

                        # Lock the door again
                        door_latch.set_status("inactive")
                        logger.info("Door locked")
                    else:
                        logger.info("Access denied")

                    # Reset variable for next iteration
                    rfid_monitor_shared_var.reset()

                # Check for updates in door_monitor_shared_var
                door_state = door_monitor_shared_var.get()
                if door_state is not None:
                    logger.info(f"Door State Updated: {door_state}")
                    # Add notification logic here
                    door_monitor_shared_var.reset()  # Reset after logging the update

            # If 'active', then run add member logic
            elif mode_state == "active":
                # Get guest ID first
                guest_obf_id = rfid_monitor_shared_var.get()

                # if guest_obf_id was scanned and the ID is not in the database
                if guest_obf_id is not None:
                    logger.info(f"Guest ID scanned: {guest_obf_id}")

                    # Assume guest is new and check if renewing temp access
                    guest_is_new = True

                    # If guest is not already in database
                    if db.get_member({"obf_rfid": obf_id}) is not None:
                        guest_is_new = False

                    logger.info("Scanning for authorizing member")

                    # Wait for authorizing member's scan
                    time.sleep(5)
                    sponsor_obf_id = rfid_monitor_shared_var.get()

                    if sponsor_obf_id is not None:
                        # Get sponsor info
                        sponsor_info = db.get_member({"obf_rfid": sponsor_obf_id})

                        if sponsor_info and sponsor_info["member_level"] == "Member":
                            logger.info(f"Sponsor authorized: {sponsor_obf_id}")
                            if guest_is_new:
                                logger.info(f"Adding guest: {guest_obf_id}. Sponsored by: {sponsor_obf_id}")
                            else:
                                logger.info(f"Updating guest: {guest_obf_id}. Sponsored by: {sponsor_obf_id}")
                        else:
                            logger.info("Sponsor not authorized")

            else:
                if mode_state is not None:
                    logger.warning(f"Unknown mode state")

            # Reset mode_switch for next iteration
            mode_monitor_shared_var.reset()
            time.sleep(0.05)
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt detected. Shutting down ADA...")

    finally:
        # Stopping the monitors before exiting (cleanup)
        rfid_monitor.stop_monitoring()
        door_monitor.stop_monitoring()
        # mode_monitor.stop_monitoring()
        GPIO.cleanup()
        logger.info("ADA shutdown completed.")


if __name__ == "__main__":
    main()