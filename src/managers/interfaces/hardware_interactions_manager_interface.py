from abc import ABC, abstractmethod

class HardwareInteractionManagerInterface(ABC):
    """
    Defines the interface for managing interactions with hardware components in the ADA system.
    This includes reading from sensors, controlling actuators, and monitoring hardware states.
    """

    @abstractmethod
    def read_rfid(self) -> str:
        """
        Initiates an RFID read operation and returns the identifier of the scanned tag.

        Returns:
        - str: The identifier of the scanned RFID tag, or None if no tag is detected.
        """
        pass

    @abstractmethod
    def unlock_door(self):
        """
        Sends a signal to unlock the door.
        """
        pass

    @abstractmethod
    def lock_door(self):
        """
        Sends a signal to lock the door.
        """
        pass

    @abstractmethod
    def monitor_door_status(self) -> str:
        """
        Monitors the current status of the door (e.g., open, closed).

        Returns:
        - str: The current door status.
        """
        pass

    @abstractmethod
    def monitor_environment(self) -> dict:
        """
        Collects and returns environmental data from various sensors (e.g., temperature, humidity, motion sensors).

        Returns:
        - dict: A dictionary containing key-value pairs of environmental data.
        """
        pass
