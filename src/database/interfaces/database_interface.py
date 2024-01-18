from abc import abstractmethod
from ...ada_interface import ADAInterface

class DatabaseInterface(ADAInterface):
    """
    DatabaseInterface is an abstract base class for database interactions within
    the ADA system. It defines a standard interface for various database operations,
    allowing for implementations that are adaptable to different database backends.

    Purpose:
    - To provide an abstract layer for database operations, enabling flexibility in
      using different database technologies.

    Abstract Methods:
    - initialize(): Set up the database connection using provided config.
    - add_member(obf_rfid, member_info): Add a new member to the database.
    - get_member(obf_rfid): Retrieve a member's details from the database.
    - update_member(obf_rfid, member_info): Update a member's record in the database.

    Usage:
    - Subclasses should provide concrete implementations for each abstract method.
    - Ensure that database connections are managed efficiently, with proper handling
      of resources and errors.

    Configurations:
    - The config parameter should include necessary details like connection strings,
      authentication info, etc., required for establishing database connections.

    Error Handling:
    - Implementations should handle database-related errors gracefully and log
      significant events or errors for troubleshooting.

    Integration:
    - DatabaseInterface implementations are typically used by other components of
      the ADA system to perform CRUD operations related to member data.

    Example:
    class MyDatabase(DatabaseInterface):
        def initialize(self):
            # Implementation details for database initialization
            pass
        # Implement other abstract methods...

    Note:
    - Be mindful of security best practices, especially when dealing with sensitive
      member data and database credentials.
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