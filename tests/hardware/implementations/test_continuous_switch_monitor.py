import unittest
from unittest.mock import Mock
from src.hardware.implementations.continuous_switch_monitor import ContinuousSwitchMonitor
import time

class TestContinuousSwitchMonitor(unittest.TestCase):
    def setUp(self):
        self.mock_switch_reader = Mock()
        self.mock_shared_state = Mock()
        self.config = {
            "name": "Mock_switch_monitor",
            "monitoring_interval": 0.1,  # A shorter interval for testing
            "threading_shared_var": self.mock_shared_state,
            "switch_reader": self.mock_switch_reader
        }
        self.switch_monitor = ContinuousSwitchMonitor(self.config)

    def test_start_and_stop_monitoring(self):
        # Simulate switch state changes
        self.mock_switch_reader.get_status.side_effect = [False, True, False, False]

        # Start monitoring
        self.switch_monitor.start_monitoring()
        time.sleep(0.35)  # Allow some time for the thread to run
        self.assertTrue(self.switch_monitor.running, "Monitoring should be running")

        # Need to see if this can be tested more accurately
        # Check if switch state changes were handled correctly
        # self.assertEqual(self.mock_switch_reader.get_status.call_count, 3, "Switch reader should have been called three times")
        # self.assertEqual(self.mock_shared_state.set.call_count, 2, "Shared state should be updated twice")
        self.assertTrue(self.mock_switch_reader.get_status.call_count >= 3, "Switch reader should have been called at least three times")

        # Stop monitoring
        self.switch_monitor.stop_monitoring()
        self.switch_monitor.monitoring_thread.join()  # Ensure the thread has finished
        self.assertFalse(self.switch_monitor.running, "Monitoring should be stopped")

    # Additional tests can be added here to further verify the behavior of ContinuousSwitchMonitor

if __name__ == '__main__':
    unittest.main()
