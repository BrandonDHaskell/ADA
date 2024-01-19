import logging
import time
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

# Pseudo Code

# main()
#   Initialize hardware and software components:
#       - DB
#       - MFRC522 Scanner
#       - Mode Switch (toggle Scan for access v Scan to add member)
#       - Add Guest Button (toggle scan guest v. scan member)
#       - Door Position Switch (Open v. Closed)
#       - Door latch (Open v. Closed)
#       - LED Screen (for printing to user)
#       - Noisebridge notifier (for notifications about door status)

#   Create thread for door monitoring
#       - this thread monitors the door and notifies Noisebridge when it is open or closed
#       - create thread from main to monitor door position
#       - add door position switch
#       - add Noisebridge notifier

#   Start main while Loop for Scanning
#       - Scan for ID
#       - If ID value returned:
#           - If Mode Switch is 'Scan for Access':
#               - Validate access with DB
#               - If Valid access:
#                   - Print: "Access granted"
#                   - Release Door latch for 7 seconds
#               - Else
#                   - Print: "No Access"
#           - ElIf Mode Switch is 'Scan to add member':
#               - Print: "Scan guest card"
#               - Scan for ID and store as Guest ID
#               - Print: "Scan NB Sponsor"
#               - Scan for ID
#               - Validate NB Sponsor ID has authority to sponsor
#               - If NB Sponsor has authority:
#                   - Save record to DB
#                   - Print QR Code
#               - If NB Sponsor does NOT have authority to sponsor:
#                   - Print: "Sponsor not authorized"

# def test_hardware(switch_reader, rfid_reader):
#     try:
#         while True:
#             # Check switch status
#             status = switch_reader.get_status()
#             logger.info(f"Switch status: {status}")

#             # Check for RFID tag
#             hashed_id = rfid_reader.scan_for_obf_id()
#             if hashed_id:
#                 logger.info(f"Detected RFID tag with hashed ID: {hashed_id}")
#             else:
#                 logger.info("No RFID tag detected.")

#             time.sleep(1)
#     except KeyboardInterrupt:
#         logger.info("Stopping switch monitoring")
#     finally:
#         switch_reader.cleanup()

def main():
    
    # Initialize database
    db_config = {
        "name": "ada_json_db",
        "connection_info": "json_database/db.json"
    }
    db = JsonDatabase(db_config)

    # Initialize a DoorReedSwitch using PiGPIOSwitchReader
    door_reed_switch_config = {
        "name": "DoorReedSwitch",
        "pin_number": 4,
        "normally_open": True,
        "common_to_ground": True
    }
    door_reed_switch = PiGPIOSwitchReader(door_reed_switch_config)

    # Initialize a ContinuousSwitchMonitor for the DoorReedSwitch
    door_monitor_shared_var = SharedVariable() # create thread safe variable for ADA to track
    door_monitor_config = {
    "name": "DoorMonitor",
    "monitoring_interval": 7,
    "threading_shared_var": door_monitor_shared_var,
    "switch_reader": door_reed_switch
    }
    door_monitor = ContinuousSwitchMonitor(door_monitor_config)

    # Initialize a ModeSwitch using PiGPIOSwitchReader
    mode_switch_config = {
        "name": "ModeSwitch",
        "pin_number": 18,
        "normally_open": True,
        "common_to_ground": True
    }
    mode_switch = PiGPIOSwitchReader(mode_switch_config)

    # Initialize a DoorLatch using PiGPIOSwitchOperator
    door_latch_config = {
        "name": "DoorLatch", 
        "pin_number": 21
    }  # Update the GPIO pin number
    door_latch = PiGPIOSwitchOperator(door_latch_config)

    # Initialize MFRC522Reader
    rfid_reader_config = {"name": "RfidReader"}
    rfid_reader = MFRC522Reader(rfid_reader_config)

    # Initialize a ContinuousSwitchMonitor for the MFRC522Reader
    rfid_monitor_shared_var = SharedVariable() # create thread safe variable for ADA to track
    rfid_monitor_config = {
    "name": "RfidMonitor",
    "monitoring_interval": 1,
    "threading_shared_var": rfid_monitor_shared_var,
    "mfrc522_reader": rfid_reader
    }
    rfid_monitor = RFIDContinuousMonitor(rfid_monitor_config)

    # Start the monitoring threads
    rfid_monitor.start_monitoring()
    door_monitor.start_monitoring()

    try:
        while True:
            # Check for updates in rfid_monitor_shared_var
            rfid_state = rfid_monitor_shared_var.get()
            if rfid_state is not None:
                logger.info(f"RFID State Updated: {rfid_state}")
                rfid_monitor_shared_var.reset()  # Reset after logging the update

            # Check for updates in door_monitor_shared_var
            door_state = door_monitor_shared_var.get()
            if door_state is not None:
                logger.info(f"Door State Updated: {door_state}")
                door_monitor_shared_var.reset()  # Reset after logging the update

            time.sleep(0.5)
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt detected. Shutting down ADA...")

    finally:
        # Stopping the monitors before exiting (cleanup)
        rfid_monitor.stop_monitoring()
        door_monitor.stop_monitoring()
        logger.info("ADA shutdown completed.")
    
    # member_info = {
    #     "obf_rfid": "1",
    #     "member_level": "value",
    #     "membership_status": "active",
    #     "member_sponsor": "sponsor_obf_rfid"
    # }
    # db.add_member(member_info)
    # member_info["obf_rfid"] = "2"
    # db.add_member(member_info)
    # member_info["obf_rfid"] = "3"
    # db.add_member(member_info)
    # member_info["obf_rfid"] = "4"
    # db.add_member(member_info)
    # member_info["obf_rfid"] = "5"
    # db.add_member(member_info)

    # # Switch reader configuration
    # switch_config = {
    #     "name": "DoorReedSwitch",
    #     "pin_number": 4,
    #     "normally_open": True,
    #     "common_to_ground": True
    # }
    # switch_reader = PiGPIOSwitchReader(switch_config)

    # rfid_config = {
    #     "name": "mfrc522Reader"
    # }
    # rfid_reader = MFRC522Reader(rfid_config)

    # # Start testing hardware
    # test_hardware(switch_reader, rfid_reader)

if __name__ == "__main__":
    main()