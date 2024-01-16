import logging
import hashlib
import base64
from mfrc522 import BasicMFRC522
from src.hardware.interfaces.rfid_reader_interface import RFIDScanner

class MFRC522Reader(RFIDScanner):
    """
    A basic implementation of an RFID reader using an MFRC522 chip on a 
    Raspberry Pi GPIO.
    """
    def __init__(sefl, config):
        super().__init__(config)
        self.reader = BasicMFRC522()
        self.initialize()

    def initialize(self):
        self.logger.info(f"{config['name']} initialized")

    def scan_for_obf_id(self):
        self.logger.info("Checking for RFID card...")
        id = self.reader.read_id_no_block()
        if id:
            hashed_id = self._hash_id(str(id))
            self.logger.info(f"RFID card detected, hashed ID: {hashed_id}")
            return hashed_id
        return None

    # Hash ID using sha256 and encode in base64
    # this could be updated to hex if needed
    def _hash_id(self, raw_id):
        hash_obj = hashlib.sha256()
        hash_obj.update(raw_id.encode('utf-8'))
        return base64.b64encode(hash_obj.digest()).decode()