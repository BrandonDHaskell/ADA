import logging
import time
from src.utils.logging_utils import setup_logging
from src.database.implementations.json_database import JsonDatabase
from src.hardware.implementations.pi_gpio_switch_reader import PiGPIOSwitchReader

# Configure basic logging for now
# TODO - make this an app configuration
setup_logging(logging.INFO)
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

def test_switch_reader(switch_reader):
    try:
        while True:
            status = switch_reader.get_status()
            logging.info(f"Switch status: {status}")
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Stopping switch monitoring")
    finally:
        switch_reader.cleanup()

def main():
    db_path = "json_database/db.json"

    db = JsonDatabase(db_path)

    member_info = {
        "obf_rfid": "1",
        "member_level": "value",
        "membership_status": "active",
        "member_sponsor": "sponsor_obf_rfid"
    }
    db.add_member(member_info)
    member_info["obf_rfid"] = "2"
    db.add_member(member_info)
    member_info["obf_rfid"] = "3"
    db.add_member(member_info)
    member_info["obf_rfid"] = "4"
    db.add_member(member_info)
    member_info["obf_rfid"] = "5"
    db.add_member(member_info)

    # Switch reader configuration
    switch_config = {
        "pin_number": 2,
        "normally_open": True,
        "common_to_ground": True
    }
    switch_reader = PiGPIOSwitchReader(switch_config)
    switch_reader.initialize(switch_config)

    # Start testing switch
    test_switch_reader(switch_reader)

if __name__ == "__main__":
    main()