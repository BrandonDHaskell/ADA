from abc import ABC, abstractmethod
from src.hardware.interfaces.hardware_interface import HardwareInterface

class ContinuousMonitoringInterface(HardwareInterface, ABC):
    """
    ContinuousMonitoringInterface is an abstract base class designed for hardware
    components that require continuous monitoring in the ADA project. It extends
    HardwareInterface, ensuring all continuous monitoring devices adhere to the
    basic hardware interface requirements.

    Purpose:
    - To provide a standardized approach for continuously monitoring hardware states,
      such as sensors or switches, and reacting to changes.

    Abstract Methods:
    - start_monitoring(): Implement the logic to start monitoring the hardware.
    - stop_monitoring(): Implement cleanup and resource release logic.

    Implementation:
    - Subclasses should implement the monitoring logic in a way that minimizes resource
      consumption and handles state changes efficiently.
    - Consider implementing the monitoring logic in a separate thread if it involves
      blocking operations or long-running loops.

    Integration:
    - This interface is typically used in conjunction with shared variables to
      communicate state changes to the main application thread.
    - A thread enabled utility variable is also availble as part of ADA

    Note:
    - Ensure that implementations are thread-safe if they operate in a multi-threaded
      environment.
    - Proper exception handling and logging are crucial for diagnosing issues in
      the field.
    """

    def __init__(self, config):
        super().__init__(config)

    @abstractmethod
    def start_monitoring(self):
        """
        This should initiate a loop that conintuously monitors a hardware deice for a state
        change.
        """
        pass

    @abstractmethod
    def stop_monitoring(self):
        """
        This should stop the loop and termintate the open thread if needed.
        """
        pass