import logging
from abc import ABC, abstractmethod
from src.utils.logging_utils import setup_logging

# Initialize logging for the entire application
setup_logging()

class ADAInterface(ABC):
    """
    ADAInterface is an abstract base class that serves as a foundational component for
    all systems interfacing with the ADA system. It standardizes logging across various
    components and ensures unique naming for instances.

    Purpose:
    - To provide a consistent logging mechanism and unique identification for each component
      in the ADA system.

    Unique Naming and Logging:
    - Each instance derived from ADAInterface must have a unique name, specified in the config.
    - If names provided are not unique, ADAInterface enforces uniqueness by appending a number
      to the name based on how many occurances have already been provided.
    - The unique name is used to create a dedicated logger for each instance, aiding in
      clear and organized logging.

    Abstract Methods:
    - initialize(): Subclasses must implement this method to define their initialization logic.

    Configuration:
    - The config parameter must include a 'name' key that is used for logging and instance
      identification.

    Usage:
    - To create a new component in the ADA system, extend ADAInterface and implement the
      required abstract methods.

    Extending the Class:
    - When extending ADAInterface, ensure that the superclass __init__ method is called with
      the appropriate config, and provide an implementation for the abstract 'initialize' method.

    Error Handling:
    - If a 'name' is not provided in the config, ADAInterface raises a ValueError.

    Instance Name Management:
    - The class method reset_instance_names() can be used to clear the set of used instance names.
      This might be useful in scenarios such as unit testing or certain application restarts.

    Example:
    class MyComponent(ADAInterface):
        def __init__(self, config):
            super().__init__(config)
        
        def initialize(self):
            # Initialization logic for MyComponent
            pass
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