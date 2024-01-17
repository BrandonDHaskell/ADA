import logging
from abc import ABC, abstractmethod
from src.utils.logging_utils import setup_logging

# Initialize logging for the entire application
setup_logging()

class ADAInterface(ABC):
    """
    An abstract base class for the ADA system.
    This class ensures all systems that interface with ADA have a unique name for logging
    and implement the same log formatting.
    """
    _instance_names = set()

    def __init__(self, config):
        """
        If the name from config is already initialized in ADA, then a numeric
        value is appended to the name making it unique.
        """
        name = self._generate_unique_name(config.get("name"))
        if not name:
            raise ValueError("A 'name' must be provided in the config")

        self.logger = logging.getLogger(name)
        self.initialize()

    @abstractmethod
    def initialize(self):
        # Initialization logic for subclasses
        pass

    @classmethod
    def _generate_unique_name(cls, base_name):
        if not base_name:
            raise ValueError("A base name must be provided in the config")

        # Ensure unique name
        counter = 1
        unique_name = base_name
        while unique_name in cls._instance_names:
            unique_name = f"{base_name}_{counter}"
            counter += 1

        cls._instance_names.add(unique_name)
        return unique_name

    # Optional: Method to reset instance names
    @classmethod
    def reset_instance_names(cls):
        cls._instance_names.clear()