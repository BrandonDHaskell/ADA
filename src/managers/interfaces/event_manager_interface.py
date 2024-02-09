from abc import ABC, abstractmethod
from typing import Callable, Any, Dict

class EventManagerInterface(ABC):
    """
    Defines the interface for managing events within the ADA system.
    This includes publishing events, subscribing to events, and unsubscribing from events.
    """

    @abstractmethod
    def publish_event(self, event_name: str, event_data: Dict[str, Any]):
        """
        Publishes an event to be consumed by any interested subscribers.

        Parameters:
        - event_name (str): The name of the event being published.
        - event_data (Dict[str, Any]): A dictionary containing the data associated with the event.
        """
        pass

    @abstractmethod
    def subscribe_to_event(self, event_name: str, callback: Callable[[Dict[str, Any]], None]):
        """
        Subscribes a callback function to a specified event. The callback will be invoked when the event is published.

        Parameters:
        - event_name (str): The name of the event to subscribe to.
        - callback (Callable[[Dict[str, Any]], None]): The callback function to be invoked when the event is published. The function should accept a single argument: a dictionary containing the event data.
        """
        pass

    @abstractmethod
    def unsubscribe_from_event(self, event_name: str, callback: Callable[[Dict[str, Any]], None]):
        """
        Unsubscribes a previously subscribed callback from a specified event.

        Parameters:
        - event_name (str): The name of the event to unsubscribe from.
        - callback (Callable[[Dict[str, Any]], None]): The callback function to be unsubscribed.
        """
        pass
