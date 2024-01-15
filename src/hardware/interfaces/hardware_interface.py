import logging
from abc import ABC, abstractmethod

"""
An abstract class base for all hardware components in the ADA system.
This should be the basic methods that all hardware uses with ADA.
"""
class HardwareInterface(ABC):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    """
    Initialize the hardware. This might be just setting the GPIO pins to use.
    """
    @abstractmethod
    def initialize(self, config_info):
        self.logger.info("Initializing hardware")