import json
from pathlib import Path
from ..interfaces.database_interface import DatabaseInterface

class JsonDatabase(DatabaseInterface):
    def __init__(self, config):
        self.filepath = Path(config["connection_info"])
        super().__init__(config)

        self.logger.debug(f"JsonDatabase initialized with config: {config}")
        self.initialize()

    def initialize(self):
        if not self.filepath.exists():
            self.logger.info(f"{self.filepath} not found. Creating a new one.")
            self.filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(self.filepath, "w") as file:
                json.dump({}, file, indent=4)
            self.logger.info(f"JSON Database file created.")
        else:
            self.logger.info("JSON database file exists.")

        self.data = self._load_data()
        self.logger.info(f"JsonDatabase loaded with file: {self.filepath}")

    def _load_data(self):
        """ 
        Load data from the JSON file
        Raises Exceptions for JSON parsing and general read error
        """       
        try:
            with open(self.filepath, "r") as file:
                self.logger.debug("Loading data from JSON file.")
                return json.load(file)
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding JSON from {self.filepath}: {e}")
            return {}
        except Exception as e:
            self.logger.error(f"Error loading data from {self.filepath}: {e}")
            return {}
        
    def _save_data(self):
        """
        Save data to the JSON file
        Raises Exception for write error
        """
        try:
            with open(self.filepath, "w") as file:
                json.dump(self.data, file, indent=4)
            self.logger.info(f"Data successfully saved to {self.filepath}")
        except Exception as e:
            self.logger.error(f"Error saving data to {self.filepath}: {e}")

    def _validate_member_info(self, member_info):
        """
        Validate that member_info contains an obfuscated RFID.
        If not, raise a ValueError
        """
        obf_rfid = member_info.get("obf_rfid")
        if not obf_rfid:
            self.logger.error("Member RFID is required")
            raise ValueError("Member RFID is required")
        return obf_rfid

    def add_member(self, member_info):
        """
        Add a new member to the database
        Raises ValueError if member already exists in database
        """

        # validate an obfuscated RFID is in member_info
        obf_rfid = self._validate_member_info(member_info)
        
        # validate obfuscated RFID is unique
        if obf_rfid in self.data:
            self.logger.error(f"Attempt to add existing member with ID {obf_rfid}")
            raise ValueError(f"Member with RFID {obf_rfid} already exists")
        
        self.data[obf_rfid] = member_info
        self._save_data()
        self.logger.info(f"Member added with RFID {obf_rfid}")
        return member_info

    def get_member(self, member_info):
        """
        Retrieve a member's details from the database
        Follows python's dictionary return results
        """

        # validate an obfuscated RFID is in member_info
        obf_rfid = self._validate_member_info(member_info)
        
        # get member_info from obfuscated RFID
        member_info = self.data.get(obf_rfid)
        if member_info:
            self.logger.debug(f"Retrieved member with ID {obf_rfid}")
        else:
            self.logger.debug(f"Member with ID {obf_rfid} not found")
        return member_info
    
    def update_member(self, member_info):
        """
        Update a member's record in the database.
        """

        # validate an obfuscated RFID is in member_info
        obf_rfid = self._validate_member_info(member_info)
        
        # validate an obfuscated RFID is in database
        if obf_rfid not in self.data:
            self.logger.error(f"Cannot update: Member with ID {obf_rfid} does not exist in the database")
            raise KeyError(f"Member with ID {obf_rfid} not found")
        
        self.data[obf_rfid].update(member_info)
        self._save_data()
        self.logger.info(f"Member with RFID {obf_rfid} updated.")
        return self.data[obf_rfid]