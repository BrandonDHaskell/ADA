from abc import ABC, abstractmethod
from typing import Dict, Optional

class DatabaseManagerInterface(ABC):
    """
    Defines the interface for managing database interactions within the ADA system.
    This includes operations on member data, access logs, and other necessary persistence functionalities.
    """

    @abstractmethod
    def add_member(self, member_data: Dict) -> bool:
        """
        Adds a new member to the database.

        Parameters:
        - member_data (Dict): A dictionary containing the member's data.

        Returns:
        - bool: True if the member was successfully added, False otherwise.
        """
        pass

    @abstractmethod
    def get_member(self, member_id: str) -> Optional[Dict]:
        """
        Retrieves a member's details from the database.

        Parameters:
        - member_id (str): The identifier of the member to retrieve.

        Returns:
        - Optional[Dict]: The member's data as a dictionary if found, None otherwise.
        """
        pass

    @abstractmethod
    def update_member(self, member_id: str, updates: Dict) -> bool:
        """
        Updates an existing member's details in the database.

        Parameters:
        - member_id (str): The identifier of the member to update.
        - updates (Dict): A dictionary containing the updates to apply to the member's data.

        Returns:
        - bool: True if the member's details were successfully updated, False otherwise.
        """
        pass

    @abstractmethod
    def delete_member(self, member_id: str) -> bool:
        """
        Deletes a member from the database.

        Parameters:
        - member_id (str): The identifier of the member to delete.

        Returns:
        - bool: True if the member was successfully deleted, False otherwise.
        """
        pass

    @abstractmethod
    def log_access_attempt(self, attempt_data: Dict) -> bool:
        """
        Logs an access attempt in the database.

        Parameters:
        - attempt_data (Dict): A dictionary containing the data of the access attempt.

        Returns:
        - bool: True if the access attempt was successfully logged, False otherwise.
        """
        pass

    @abstractmethod
    def query_access_logs(self, criteria: Dict) -> Optional[list]:
        """
        Queries access logs based on specified criteria.

        Parameters:
        - criteria (Dict): A dictionary specifying the criteria for filtering access logs.

        Returns:
        - Optional[list]: A list of access logs that match the criteria, None if no logs match.
        """
        pass
