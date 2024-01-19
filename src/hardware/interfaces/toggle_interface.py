from abc import abstractmethod
from src.hardware.interfaces.hardware_interface import HardwareInterface

class ToggleReaderInterface(HardwareInterface):
    """
    ToggleReaderInterface is an abstract class for components responsible for 
    reading the status of hardware toggles, such as switches or pins, in the ADA system.

    Abstract Methods:
    - initialize(): Prepare any necessary configurations for the toggle reader.
    - get_status(): Retrieve the current status ('active' or 'inactive') of the toggle.

    Usage:
    - Extend this interface to implement specific logic for different types of toggle readers.
    - Ensure robust error handling and logging for reliable operation.

    Example:
    class MySwitchReader(ToggleReaderInterface):
        def initialize(self):
            # Specific initialization logic
            pass
        def get_status(self):
            # Logic to read the switch status
            pass
    """

    def __init__(self, config):
        super().__init__(config)
        self.config = config
        self.initialize()

    @abstractmethod
    def initialize(self):
        """
        Initialize the toggle reader.
        Implementations should log the successful initialization or any errors.
        :param config: Information needed to configure the toggle reader
        """
        pass

    @abstractmethod
    def get_status(self):
        """
        Method to get the status of the toggle reader.
        :return: current toggle status: 'active' or 'inactive'
        """
        pass

class ToggleOperatorInterface(HardwareInterface):
    """
    ToggleOperatorInterface is an abstract class for components that operate or set 
    the status of hardware toggles, like switches, pins, or lights, in the ADA system.

    Abstract Methods:
    - initialize(): Set up the toggle operator with necessary configurations.
    - set_status(new_state): Change the status of the toggle to 'active' or 'inactive'.

    Usage:
    - Implement this interface for hardware components that need to control toggles.
    - Pay attention to thread safety and synchronization if toggles are accessed from
      multiple threads.

    Example:
    class MySwitchOperator(ToggleOperatorInterface):
        def initialize(self):
            # Specific initialization logic
            pass
        def set_status(self, new_state):
            # Logic to set the switch status
            pass
    """

    def __init__(self, config):
        super().__init__(config)
        self.config = config
        self.initialize()

    @abstractmethod
    def initialize(self):
        """
        Initialize the toggle operator.
        Implementations should log the successful initialization or any errors.
        :param config: Information needed to configure the toggle operator
        """
        pass

    @abstractmethod
    def set_status(self, new_state):
        """
        Method to set the status of the toggle operator.
        :param new_state: the new status of the toggle: 'active' or 'inactive'
        """
        pass