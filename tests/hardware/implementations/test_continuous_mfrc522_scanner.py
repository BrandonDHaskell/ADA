import unittest
from unittest.mock import Mock, patch
from src.hardware.implementations.continuous_mfrc522_scanner import RFIDContinuousMonitor
import time

class TestRFIDContinuousMonitor(unittest.TestCase):
    def setUp(self):
        self.mock_mfrc522_reader = Mock()
        self.mock_shared_state = Mock()
        self.config = {
            "name": "Mock_mfrc522_reader",
            "monitoring_interval": 0.1,  # A shorter interval for testing
            "threading_shared_var": self.mock_shared_state,
            "mfrc522_reader": self.mock_mfrc522_reader
        }
        self.rfid_monitor = RFIDContinuousMonitor(self.config)

    def test_start_and_stop_monitoring(self):
        # Simulate a scanned RFID tag
        self.mock_mfrc522_reader.scan_for_obf_id.return_value = "hashed_rfid_id"

        # Start monitoring
        self.rfid_monitor.start_monitoring()
        time.sleep(0.3)  # Allow some time for the thread to run
        self.assertTrue(self.rfid_monitor.running, "Monitoring should be running")

        # Check if RFID scan was successful
        self.mock_mfrc522_reader.scan_for_obf_id.assert_called()
        self.mock_shared_state.set.assert_called_with("hashed_rfid_id")

        # Stop monitoring
        self.rfid_monitor.stop_monitoring()
        self.rfid_monitor.monitoring_thread.join()  # Ensure the thread has finished
        self.assertFalse(self.rfid_monitor.running, "Monitoring should be stopped")

    # Additional tests can be added here to further verify the behavior of RFIDContinuousMonitor

if __name__ == '__main__':
    unittest.main()
