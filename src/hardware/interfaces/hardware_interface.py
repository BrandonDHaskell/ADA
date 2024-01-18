from abc import ABC, abstractmethod
from ...ada_interface import ADAInterface

class HardwareInterface(ADAInterface):
    """
    An abstract class base for all hardware components in the ADA system.
    This should be the basic methods that all hardware uses with ADA.
    """

    def __init__(self, config):
        # Initialize the ADAInterface with the provided config
        super().__init__(config)

        self.initialize()
        
    """
    Initialize the hardware. This might be just setting the GPIO pins to use.
    """
    @abstractmethod
    def initialize(self):
        self.logger.debug("Initializing hardware")