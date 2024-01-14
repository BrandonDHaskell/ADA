import pytest
from src.database.json_database import JsonDatabase

def test_add_member():
    db = JsonDatabase("test_db.json")
    member_info = {
        "obf_rfid": "1234567890",
        "member_level": "value",
        "membership_status": "active",
        "member_sponsor": "sponsor_obf_rfid"
    }
    assert db.add_member(member_info) == member_info

def test_add_existing_member():
    db = JsonDatabase("test_db.json")
    member_info = {
        "obf_rfid": "1234567890",
        "member_level": "value",
        "membership_status": "active",
        "member_sponsor": "sponsor_obf_rfid"
    }
    db.add_member(member_info)
    with pytest.raises(ValueError):
        db.add_member(member_info)