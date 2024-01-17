import pytest
from src.database.interfaces.database_interface import DatabaseInterface

# Mock implementation of DatabaseInterface for testing
class MockDatabase(DatabaseInterface):
    def __init__(self):
        # Assuming no actual connection info is needed for the mock, pass a dummy value
        dummy_connection_info = {"name": "mock_database", "connection_info": "dummy_connection_info"}
        super().__init__(dummy_connection_info)

    def initialize(self):
        pass

    def add_member(self, obf_rfid, member_info):
        pass

    def get_member(self, obf_rfid):
        pass

    def update_member(self, obf_rfid, member_info):
        pass

def test_database_interface_implementations():
    """
    Test that MockDatabase implements all abstract methods of DatabaseInterface
    """
    assert issubclass(MockDatabase, DatabaseInterface)

def test_database_interface_methods():
    """
    Test that the mock implementation can be instantiated and has the expected methods.
    """
    mock_db = MockDatabase()
    assert hasattr(mock_db, "initialize")
    assert hasattr(mock_db, "add_member")
    assert hasattr(mock_db, "get_member")
    assert hasattr(mock_db, "update_member")