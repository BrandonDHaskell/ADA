from abc import abstractmethod
from ...ada_interface import ADAInterface

class HardwareInterface(ADAInterface):
    """
    HardwareInterface serves as an abstract base class for all hardware components
    within the ADA system. It extends the ADAInterface to ensure consistent logging
    and initialization across all hardware-related classes.

    Purpose:
    - To define a common interface for all hardware components in the system.
    - To ensure standardized logging and initialization procedures.

    Usage:
    - HardwareInterface is not intended to be instantiated directly.
    - Instead, create a subclass for each specific type of hardware component and 
      implement the required abstract methods.

    Abstract Methods:
    - initialize(): Each subclass must provide an implementation for hardware 
      initialization. This could include setting up GPIO pins, establishing 
      network connections, configuring sensors, etc.

    Example:
    class MyCustomSensor(HardwareInterface):
        def initialize(self):
            # Custom initialization for MyCustomSensor
            pass

    Note:
    - When implementing the initialize method, consider all necessary setup steps 
      for your hardware to function correctly.
    - Ensure that any resources allocated during initialization are properly 
      managed and released when no longer needed.

    Integration:
    - Subclasses of HardwareInterface are typically instantiated and used by other 
      components of the ADA system that interact with hardware.
    - The logging provided by ADAInterface should be used for consistency and 
      debugging purposes.

    Exception Handling:
    - Proper error handling in the initialize method and other parts of your hardware 
      implementation is crucial. Always log significant events and errors.
    """
    
    def __init__(self, config):
        # Initialize the ADAInterface with the provided config
        super().__init__(config)
        
    @abstractmethod
    def initialize(self):
        # Implement initialization logic specific to the hardware component.
        # It is recommended to include logging in the implementation to track
        # the initialization process and any potential issues.
        pass
