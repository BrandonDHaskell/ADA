import logging
from abc import abstractmethod
from src.hardware.interfaces.hardware_interface import HardwareInterface

class ToggleReaderInterface(HardwareInterface):
    """
    An abstract class for reading hardware toggles (aka switches, pins, etc.)
    """

    def __init__(self, config_info):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config_info = config_info
        self.logger.info(f"Initializing toggle reader with config info: {config_info}")
        self.initialize(config_info)

    @abstractmethod
    def initialize(self):
        self.logger.info("Initializing toggle reader")
        """
        Initialize the toggle reader.
        Implementations should log the successful initialization or any errors.
        :param config_info: Information needed to configure the toggle reader
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
    An abstract class for operating/setting hardware toggles (aka switches, pins, lights, etc.)
    """

    def __init__(self, config_info):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config_info = config_info
        self.logger.info(f"Initializing toggle operator with config info: {config_info}")
        self.initialize(config_info)

    @abstractmethod
    def initialize(self):
        self.logger.info("Initializing toggle operator")
        """
        Initialize the toggle operator.
        Implementations should log the successful initialization or any errors.
        :param config_info: Information needed to configure the toggle operator
        """
        pass

    @abstractmethod
    def set_status(self, new_state):
        """
        Method to set the status of the toggle operator.
        :param new_state: the new status of the toggle: 'active' or 'inactive'
        """
        pass