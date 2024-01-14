import logging
import json
from pathlib import Path
from database_interface import DatabaseInterface

class JsonDatabase(DatabaseInterface):
    def __init__(self, filepath):
        super().__init__(filepath)
        self.filepath = Path(filepath)
        self.data = self._load_data()

    def _load_data(self):
        """ 
        Load data from the JSON file
        Raises Exceptions for JSON parsing and general read error
        """
        if not self.filepath.exists():
            self.logger.info(f"Database file {self.filepath} not found. Creating a new one.")
            return {}
        
        try:
            with open(self.filepath, "r") as file:
                self.logger.info("Database loaded")
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

    def add_member(self, obf_rfid, member_info):
        """
        Add a new member to the database
        Raises ValueError if member already exists in database
        """
        if obf_rfid in self.data:
            self.logger.error(f"Member with ID {obf_rfid} already exists in database")
            raise ValueError(f"Member with RFID {obf_rfid} already exists")
        
        self.data[obf_rfid] = member_info
        self._save_data()
        self.logger.info(f"Member added with RFID {obf_rfid}")

    def get_member(self, obf_rfid):
        """
        Retrieve a member's details from the database
        Follows python's dictionary return results
        """
        member = self.data.get(obf_rfid)
        if member:
            self.logger.info(f"Retrieved member with ID {obf_rfid}")
        else:
            self.logger.warn(f"Member with ID {obf_rfid} not found")
        return member
    
    def update_member(self, obf_rfid, member_info):
        """
        Update a member's record in the database.
        """
        if obf_rfid not in self.data:
            self.logger.error(f"Cannot update: Member with ID {obf_rfid} does not exist in the database")
            raise KeyError(f"Member with ID {obf_rfid} not found")
        
        self.data[obf_rfid].update(member_info)