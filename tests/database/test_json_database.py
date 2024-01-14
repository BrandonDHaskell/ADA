import pytest
from src.database.json_database import JsonDatabase
from pathlib import Path

@pytest.fixture
def db():
    # Path to create temp database
    db_path = Path("tests/database/test_db.json")
    
    # Setup: Create a temp JsonDatabase instance
    database = JsonDatabase(db_path)

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
        "member_sponsor": "sponsor_obf_rfid"
    }
    assert db.add_member(member_info) == member_info

def test_add_existing_member(db):
    member_info = {
        "obf_rfid": "1234567891",
        "member_level": "value",
        "membership_status": "active",
        "member_sponsor": "sponsor_obf_rfid"
    }
    db.add_member(member_info)
    with pytest.raises(ValueError) as e:
        db.add_member(member_info)