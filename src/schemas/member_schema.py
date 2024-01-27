member_schema = {
    "obf_rfid": str,            # obfuscated RFID
    "member_level": str,        # determined member level: 'guest', 'philanthropist','member', 'admin'
    "membership_status": str,   # determines member status: 'active' or 'inactive'
    "access_interval": str,     # determines temporary access interval (follows ISO 8601 repeating interval format: R/YYYY-MM-DDTHH:MM/P5DT10)
    "member_sponsor": str,      # member who sponsored this member (their obfuscated RFID)
    "created": str,             # Read only, should be set by the DB (follows ISO 8601 timestamp format)
    "last_updated": str         # Read only, should be set by the DB (follows ISO 8601 timestamp format)
}