from abc import abstractmethod
from src.hardware.interfaces.continuous_monitoring_interface import ContinuousMonitoringInterface
from src.utils.threading_shared_variable import SharedVariable

class ToggleMonitoringInterface(ContinuousMonitoringInterface):
    """
    ToggleMonitoringInterface is an abstract base class designed for components that 
    require continuous monitoring of toggle switches or similar hardware in the ADA project.
    It extends ContinuousMonitoringInterface to include specific functionalities for 
    toggle state monitoring.

    Purpose:
    - To provide a standardized approach for continuously monitoring the state of toggle switches,
      ensuring thread-safe communication of state changes.
    - Designed to abstract the complexity of continuous toggle monitoring and
      provide a unified interface for different types of toggle switches.

    Thread Safety:
    - Uses SharedVariable utility to safely communicate state changes between different threads.

    Abstract Methods:
    - _read_current_state(): Subclasses should implement this method to read the current state
      from the toggle switch hardware.
    - start_monitoring(), stop_monitoring(): Inherited from ContinuousMonitoringInterface, to be
      implemented for starting and stopping the monitoring process.
    - stop_monitoring(): Implement logic to stop the monitoring process and perform any necessary
      cleanup.

    Key Methods:
    - get_toggle_status(): Returns the current state of the toggle switch only if
      it has changed from the previous state. Utilizes SharedVariable for
      communicating the updated state.
    - update_shared_state(): A utility method to update the shared state if there
      is a change in the toggle switch's status.

    Usage:
    - Create a subclass implementing the specific logic for monitoring a type of toggle switch.
    - Use SharedVariable for thread-safe state communication.

    Example:
    class MyToggleSwitch(ToggleMonitoringInterface):
        def _read_current_state(self):
            # Implementation to read the state of MyToggleSwitch
            pass
        # Implement other abstract methods...

    Note:
    - Implementations should consider efficient and reliable ways to monitor the toggle state,
      minimizing resource usage while maintaining responsiveness.
    - Proper logging, error handling, and exception management are crucial for diagnosing issues
      and ensuring stable operation.
    - Ensure that the implementation adheres to the interface contract and correctly communicates
      state changes through SharedVariable.
    """

    def __init__(self, config):
        super().__init__(config)
        self._last_state = None
        self.shared_state = config.get("threading_shared_var")

    def get_toggle_status(self):
        current_state = self._read_current_state()
        if current_state != self._last_state:
            self._last_state = current_state
            self.shared_state.set(current_state)
            return current_state
        return None

    def update_shared_state(self):
        # Call this method to update the shared state if needed
        new_state = self.get_toggle_status()
        if new_state is not None:
            self.shared_state.set(new_state)

    @abstractmethod
    def _read_current_state(self):
        pass

    @abstractmethod
    def start_monitoring(self):
        pass

    @abstractmethod
    def stop_monitoring(self):
        pass
