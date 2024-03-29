import pytest
from src.database.implementations.json_database import JsonDatabase
from pathlib import Path

@pytest.fixture
def db():
    # Path to create temp database
    db_path = Path("tests/database/test_db.json")
    
    # Create config dictionary for JsonDatabase
    config = {
        "name": "test_json_db",
        "connection_info": db_path
    }

    # Setup: Create a temp JsonDatabase instance
    database = JsonDatabase(config)

    # Yield database to the test
    yield database

    # Teardown: Delete JSON after the test
    if db_path.exists():
        db_path.unlink()


def test_add_member(db):
    member_info = {
        "obf_rfid": "1234567890",
        "member_level": "value",
        "membership_status": "active",
        "access_interval": "R5/2024-02-08T11:00:00+00:00/PT9H",
        "member_sponsor": "sponsor_obf_rfid",
        "created": "",
        "last_updated":""
    }
    assert db.add_member(member_info) == member_info

def test_add_existing_member(db):
    member_info = {
        "obf_rfid": "1234567891",
        "member_level": "value",
        "membership_status": "active",
        "access_interval": "R5/2024-02-08T11:00:00+00:00/PT9H",
        "member_sponsor": "sponsor_obf_rfid",
        "created": "",
        "last_updated":""
    }
    db.add_member(member_info)
    with pytest.raises(ValueError) as e:
        db.add_member(member_info)

def test_update_member(db):
    member_info = {
        "obf_rfid": "1234567891",
        "member_level": "value",
        "membership_status": "active",
        "access_interval": "R5/2024-02-08T11:00:00+00:00/PT9H",
        "member_sponsor": "sponsor_obf_rfid",
        "created": "",
        "last_updated":""
    }
    member_update_info = {
        "obf_rfid": "1234567891",
        "member_level": "value",
        "membership_status": "inactive",
        "access_interval": "R5/2024-02-08T11:00:00+00:00/PT9H",
        "member_sponsor": "sponsor_obf_rfid",
        "created": "",
        "last_updated":""
    }
    with pytest.raises(KeyError) as e:
        db.update_member(member_info)
    
    db.add_member(member_info)
    assert db.update_member(member_update_info) == member_update_info