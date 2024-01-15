import logging
from abc import ABC, abstractmethod

class DatabaseInterface(ABC):
    """
    Abstract base class for database interactions for the ADA system.
    This interface is designed to be adaptable to various database backends.
    """

    def __init__(self, connection_info):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.connection_info = connection_info
        self.logger.info(f"Initializing database with connection info: {connection_info}")
        self.initialize(connection_info)

    @abstractmethod
    def initialize(self, connection_info):
        """
        Initialize the database connection.
        Implementations should log the successful initialization or any errors.
        :param connection_info: Information required to establish a connection to the database.
        """
        pass

    @abstractmethod
    def add_member(self, obf_rfid, member_info):
        """
        Add a new member to the database.
        Implementations should log this operation.
        :param obf_rfid: The obfuscated RFID of the member.
        :param member_info: Dictionary containing member information.
        :return: member_info object if member successfully added.
        :raises ValueError: if obf_rfid is not included in request.
        :raises ValueError: if a member with the same RFID already exists.
        """
        pass

    @abstractmethod
    def get_member(self, obf_rfid):
        """
        Retrieve a member's details from the database.
        Implementations should log the retrieval operation.
        :param obf_rfid: The obfuscated RFID of the member.
        :return: member_info object or error if the database was not updated.
        :raises ValueError: if obf_rfid is not included in request.
        """
        pass

    @abstractmethod
    def update_member(self, obf_rfid, member_info):
        """
        Update a member's record in the database.
        Implementations should log the update operation.
        :param obf_rfid: The obfuscated RFID of the member.
        :param member_info: Dictionary containing member information to update.
        :return: member_info object or error if the database was not updated.
        :raises ValueError: if obf_rfid is not included in request.
        """
        pass