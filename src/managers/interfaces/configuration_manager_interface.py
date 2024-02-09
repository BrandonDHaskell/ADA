from abc import ABC, abstractmethod
from typing import Any, Dict

class ConfigurationManagerInterface(ABC):
    """
    Defines the interface for managing configuration settings within the ADA system.
    This includes operations to retrieve configuration values, update settings, and
    potentially notify components of configuration changes.
    """

    @abstractmethod
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """
        Retrieves the value for a given configuration key.

        Parameters:
        - key (str): The configuration key for which the value is requested.
        - default (Any): The default value to return if the key does not exist.

        Returns:
        - Any: The value of the configuration setting, or the specified default value if the key is not found.
        """
        pass

    @abstractmethod
    def set_config_value(self, key: str, value: Any):
        """
        Sets or updates the value for a given configuration key.

        Parameters:
        - key (str): The configuration key to be set or updated.
        - value (Any): The value to assign to the key.
        """
        pass

    @abstractmethod
    def load_configuration(self, source: str):
        """
        Loads configuration settings from a specified source, such as a file or environment variables.

        Parameters:
        - source (str): The source from which to load configuration settings, which could be a file path or an identifier for environment variables.
        """
        pass

    @abstractmethod
    def get_all_configurations(self) -> Dict[str, Any]:
        """
        Retrieves all configuration settings currently loaded into the system.

        Returns:
        - Dict[str, Any]: A dictionary containing all configuration key-value pairs.
        """
        pass
