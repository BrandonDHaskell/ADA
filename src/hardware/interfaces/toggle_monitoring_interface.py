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

    Thread Safety:
    - Uses SharedVariable utility to safely communicate state changes between different threads.

    Abstract Methods:
    - _read_current_state(): Subclasses should implement this method to read the current state
      from the toggle switch hardware.
    - start_monitoring(), stop_monitoring(): Inherited from ContinuousMonitoringInterface, to be
      implemented for starting and stopping the monitoring process.
    - get_toggle_status(): Should return the current state of the toggle switch only if it has changed
      from the previous state.

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
    - Ensure that implementations handle hardware interactions and state changes efficiently and 
      safely, particularly in multi-threaded scenarios.
    - Proper logging and error handling are essential for reliable operation and troubleshooting.
    """

    def __init__(self, config):
        super().__init__(config)
        self._last_state = None
        self.shared_state = SharedVariable()

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
