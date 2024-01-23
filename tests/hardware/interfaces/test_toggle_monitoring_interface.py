import unittest
from unittest.mock import Mock
from src.hardware.interfaces.toggle_monitoring_interface import ToggleMonitoringInterface

class MockToggleMonitor(ToggleMonitoringInterface):
    def __init__(self, config):
        super().__init__(config)
        self.mock_state = None  # Mock state to simulate hardware toggle state

    def _read_current_state(self):
        return self.mock_state

    def start_monitoring(self):
        # Mock implementation of starting monitoring
        pass

    def stop_monitoring(self):
        # Mock implementation of stopping monitoring
        pass

    def initialize(self):
        # Mock implementation of initialize method
        pass

    # Method to simulate state change in tests
    def set_mock_state(self, state):
        self.mock_state = state

class TestToggleMonitoringInterface(unittest.TestCase):
    def setUp(self):
        shared_variable = Mock()
        config = {
            "threading_shared_var": shared_variable,
            "name": "MockToggleMonitor"  # Provide a name for the mock monitor
        }
        self.mock_monitor = MockToggleMonitor(config)

    def test_get_toggle_status_initial_state(self):
        self.assertIsNone(self.mock_monitor.get_toggle_status(), "Initial state should be None")

    def test_get_toggle_status_state_change(self):
        self.mock_monitor.set_mock_state(True)
        self.assertTrue(self.mock_monitor.get_toggle_status(), "State should be True after change")
        self.mock_monitor.set_mock_state(False)
        self.assertFalse(self.mock_monitor.get_toggle_status(), "State should be False after change")

    def test_update_shared_state(self):
        self.mock_monitor.set_mock_state(True)
        self.mock_monitor.update_shared_state()
        self.assertTrue(self.mock_monitor.shared_state.set.called, "Shared state should be updated")


if __name__ == '__main__':
    unittest.main()
