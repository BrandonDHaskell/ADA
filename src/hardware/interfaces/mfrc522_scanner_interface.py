import logging
from hardware_interface import HardwareInterface

class MFRC522Scanner(HardwareInterface):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def initialize(self):
        self.logger.info("Initializing MFRC522 scanner")
        # TODO - add initialization process