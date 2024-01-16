import logging
from abc import abstractmethod
from src.hardware.interfaces.hardware_interface import HardwareInterface

class MFRC522Scanner(HardwareInterface):
    """
    An abstract class for RFID card readers or similar hardware.
    This should scan an id and hash it before returning.
    """
    def __init__(self, config):
        super.__init__(config)

    @abstractmethod
    def initialize(self):
        self.logger.info("Initializing RFID scanner")

    @abstractmethod
    def scan_for_obf_id(self):
        """
        Scan an id, hash it then return the hashed value.
        :return: hashed ID or None if no ID was scanned
        """
        pass