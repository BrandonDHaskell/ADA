from abc import ABC, abstractmethod
from typing import Dict, Optional, List

class MemberManagementManagerInterface(ABC):
    """
    Defines the interface for managing member-related operations within the ADA system.
    This includes adding new members, updating member details, managing member statuses,
    and handling membership renewals or expirations.
    """

    @abstractmethod
    def add_new_member(self, member_data: Dict) -> bool:
        """
        Adds a new member to the system with the provided member details.

        Parameters:
        - member_data (Dict): A dictionary containing the necessary details for the new member.

        Returns:
        - bool: True if the member was successfully added, False otherwise.
        """
        pass

    @abstractmethod
    def update_member_details(self, member_id: str, updates: Dict) -> bool:
        """
        Updates details for an existing member identified by member_id.

        Parameters:
        - member_id (str): The unique identifier of the member whose details are to be updated.
        - updates (Dict): A dictionary containing the updates to be applied to the member's details.

        Returns:
        - bool: True if the updates were successfully applied, False otherwise.
        """
        pass

    @abstractmethod
    def change_member_status(self, member_id: str, new_status: str) -> bool:
        """
        Changes the membership status of a member (e.g., active, inactive, suspended).

        Parameters:
        - member_id (str): The unique identifier of the member whose status is to change.
        - new_status (str): The new status to assign to the member.

        Returns:
        - bool: True if the status was successfully changed, False otherwise.
        """
        pass

    @abstractmethod
    def adjust_member_access_level(self, member_id: str, new_level: str) -> bool:
        """
        Adjusts the access level of a member (e.g., guest, member, admin).

        Parameters:
        - member_id (str): The unique identifier of the member whose access level is to be adjusted.
        - new_level (str): The new access level to assign to the member.

        Returns:
        - bool: True if the access level was successfully adjusted, False otherwise.
        """
        pass

    @abstractmethod
    def list_members_by_status(self, status: str) -> Optional[List[Dict]]:
        """
        Retrieves a list of members filtered by their membership status.

        Parameters:
        - status (str): The membership status to filter by (e.g., active, inactive).

        Returns:
        - Optional[List[Dict]]: A list of dictionaries, each representing a member matching the specified status, or None if no members match.
        """
        pass

    @abstractmethod
    def renew_member_membership(self, member_id: str, renewal_terms: Dict) -> bool:
        """
        Processes membership renewal for a member based on specified renewal terms.

        Parameters:
        - member_id (str): The unique identifier of the member renewing their membership.
        - renewal_terms (Dict): A dictionary containing the terms of the membership renewal (e.g., duration, fees).

        Returns:
        - bool: True if the membership was successfully renewed, False otherwise.
        """
        pass
