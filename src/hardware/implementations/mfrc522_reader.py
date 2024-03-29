import hmac
import base64
import os
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from src.hardware.interfaces.rfid_reader_interface import RFIDScanner

class MFRC522Reader(RFIDScanner):
    """
    A basic implementation of an RFID reader using an MFRC522 chip on a 
    Raspberry Pi GPIO.
    """
    def __init__(self, config):
        self.config = config
        super().__init__(config)
        self.reader = SimpleMFRC522()
        self.secret_key = config.get('hmac_secret_key', os.getenv('HMAC_SECRET_KEY', 'default_secret_key'))
        self.initialize()

    def initialize(self):
        self.logger.info(f"{self.config['name']} initialized")

    def scan_for_obf_id(self):
        self.logger.debug("Checking for RFID card...")
        id = self.reader.read_id_no_block()
        if id:
            hashed_id = self._hash_id(str(id))
            self.logger.debug(f"RFID card detected, hashed ID: {hashed_id}")
            return hashed_id
        return None

    # Hash ID using sha256 and encode in base64
    # this could be updated to hex if needed
    def _hash_id(self, raw_id):
        hmac_obj = hmac.new(self.secret_key.encode("utf-8"), msg=raw_id.encode("utf-8"), digestmod="sha256")
        return hmac_obj.hexdigest()
    
    def cleanup(self):
        # Cleanup GPIO resources
        # GPIO.cleanup()
        self.logger.info("GPIO resources cleaned up")