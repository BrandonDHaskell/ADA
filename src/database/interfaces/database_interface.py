from abc import abstractmethod
from ...ada_interface import ADAInterface

class DatabaseInterface(ADAInterface):
    """
    Abstract base class for database interactions for the ADA system.
    This interface is designed to be adaptable to various database backends.
    """

    def __init__(self, config):
        super().__init__(config)
        self.config = config
        self.connection_info = config["connection_info"]
        self.initialize()

    @abstractmethod
    def initialize(self):
        """
        Initialize the database connection.
        Implementations should log the successful initialization or any errors.
        :param connection_info: Information required to establish a connection to the database.
        """
        self.logger.debug(f"Initializing  with config info: {self.config}")

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