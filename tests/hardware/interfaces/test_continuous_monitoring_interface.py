import unittest
from unittest.mock import Mock
from src.hardware.interfaces.continuous_monitoring_interface import ContinuousMonitoringInterface

class MockContinuousMonitor(ContinuousMonitoringInterface):
    def __init__(self, config):
        super().__init__(config)
        self.monitoring = False
        self.initialized = False

    def initialize(self):
        self.initialized = True

    def start_monitoring(self):
        if not self.initialized:
            raise Exception("Monitor not initialized")
        self.monitoring = True

    def stop_monitoring(self):
        if not self.initialized:
            raise Exception("Monitor not initialized")
        self.monitoring = False

class TestContinuousMonitoringInterface(unittest.TestCase):
    def setUp(self):
        config = {
            "name": "MockContinuousMonitor",  # Assuming a name key is required as per your ADAInterface
            "monitoring_interval": 2  # Add other necessary configuration keys if needed
        }
        self.mock_monitor = MockContinuousMonitor(config)
        self.mock_monitor.initialize()

    def test_start_monitoring(self):
        self.mock_monitor.start_monitoring()
        self.assertTrue(self.mock_monitor.monitoring, "Monitoring should be set to True after starting")

    def test_stop_monitoring(self):
        self.mock_monitor.stop_monitoring()
        self.assertFalse(self.mock_monitor.monitoring, "Monitoring should be set to False after stopping")

if __name__ == '__main__':
    unittest.main()
