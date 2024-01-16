import logging
from abc import ABC, abstractmethod

"""
An abstract class base for all hardware components in the ADA system.
This should be the basic methods that all hardware uses with ADA.
"""
class HardwareInterface(ABC):
    def __init__(self, config):
        if not config.get("name"):
            raise ValueError("A 'name' must be provided in the config")
        
        self.name = config["name"]
        self.logger = logging.getLogger(self.name)

        self.initialize()
        
    """
    Initialize the hardware. This might be just setting the GPIO pins to use.
    """
    @abstractmethod
    def initialize(self):
        self.logger.info("Initializing hardware")