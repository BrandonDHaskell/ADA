from abc import ABC, abstractmethod

"""
An abstract class base for all hardware components in the ADA system.
This should be the basic methods that all hardware uses with ADA.
"""
class HardwareInterface(ABC):
    """
    Initialize the hardware. This might be just setting the GPIO pins to use.
    """
    @abstractmethod
    def initialize(self):
        pass
    