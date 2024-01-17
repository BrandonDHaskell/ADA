import pytest
from src.hardware.interfaces.toggle_interface import ToggleReaderInterface, ToggleOperatorInterface

"""
Create classes of each type that mock the actual
"""
class MockToggleReader(ToggleReaderInterface):
    def __init__(self, config):
        super().__init__(config)
        # Assuming config is a dictionary with a key 'pin_number'
        self.pin_number = config.get("pin_number")
        
    def initialize(self):
        pass

    def get_status(self):
        return "active"  # Mock return value for testing
    
class MockToggleOperator(ToggleOperatorInterface):
    def initialize(self):
        pass

    def set_status(self, new_state):
        # Mock implementation for testing
        return new_state

"""
Define configs for each toggle type
"""
@pytest.fixture
def mock_reader_config():
    return {"name": "TestReader", "pin_number": 5}

@pytest.fixture
def mock_operator_config():
    return {"name": "TestOperator", "pin_number": 5}


def test_toggle_reader_initialization(mock_reader_config):
    mock_config = {"name": "TestReader", "pin_number": 5}
    reader = MockToggleReader(mock_reader_config)
    assert reader.pin_number == mock_reader_config["pin_number"]
    # Assuming the default status should be 'active' after initialization
    assert reader.get_status() == "active"

def test_toggle_reader_get_status(mock_reader_config):
    mock_config = {"name": "TestReader", "pin_number": 5}
    reader = MockToggleReader(mock_reader_config)
    assert reader.get_status() == "active"

def test_toggle_operator_initialization():
    operator = MockToggleOperator(mock_operator_config)
    assert operator.pin_number == mock_operator_config["pin_number"]
    # Check if the status can be set correctly
    operator.set_status("active")
    # Assuming there's a way to retrieve the current status, e.g., a status attribute
    assert operator.status == "active"

def test_toggle_operator_set_status():
    operator = MockToggleOperator(mock_operator_config)
    assert operator.set_status("active") == "active"