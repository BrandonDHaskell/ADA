import logging
from hardware_interface import HardwareInterface

class ToggleReader(HardwareInterface):
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def initialize(self):
        self.logger.info("Initializing toggle reader")
        # TODO - add initialization process