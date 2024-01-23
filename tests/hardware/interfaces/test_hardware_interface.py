import unittest
from unittest.mock import Mock
from src.hardware.interfaces.hardware_interface import HardwareInterface

class MockHardware(HardwareInterface):
    def initialize(self):
        # Mock implementation of initialize
        pass

class TestHardwareInterface(unittest.TestCase):
    def setUp(self):
        config = {"name": "MockHardwareName"}
        self.mock_hardware = MockHardware(config)

    def test_initialization(self):
        # Test to ensure that the mock hardware is initialized correctly
        self.assertIsInstance(self.mock_hardware, HardwareInterface, "MockHardware should be an instance of HardwareInterface")

if __name__ == '__main__':
    unittest.main()
