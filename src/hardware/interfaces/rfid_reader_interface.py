from abc import abstractmethod
from src.hardware.interfaces.hardware_interface import HardwareInterface

class RFIDScanner(HardwareInterface):
    """
    RFIDScanner is an abstract class that defines the basic structure and capabilities that any
    RFID reading hardware should implement to integrate with the ADA system.

    The primary functionality of an RFIDScanner is to scan RFID tags and return a hashed version
    of the tag's ID. This hashing is crucial for maintaining the privacy and security of the ID.

    Subclasses implementing this interface should provide concrete implementations for the
    abstract methods defined here.

    Methods:
    - initialize(): Should include any initialization logic required for the RFID scanner.
    - scan_for_obf_id(): Should implement the logic to scan an RFID tag, hash its ID, and return
      the hashed value.

    Usage:
    - Subclasses should override initialize() to set up any necessary configurations or
      initializations specific to the RFID scanner hardware.
    - scan_for_obf_id() should be implemented to read an RFID tag, apply a hashing algorithm to
      its ID, and return the hashed value. This method should return None if no ID was scanned.

    Note:
    - The choice of hashing algorithm and its implementation details are left to the subclass.
    - Ensure that the hashing method is consistent and secure to protect the identities associated
      with RFID tags.
    """
    def __init__(self, config):
        super().__init__(config)

    @abstractmethod
    def initialize(self):
        """
        Initialize the RFID scanner hardware.
        This method should set up the scanner, ensuring it is ready to scan tags.
        """
        pass

    @abstractmethod
    def scan_for_obf_id(self):
        """
        Scan an RFID tag and return a hashed version of its ID.

        The method should implement the logic to wait for an RFID tag, read its ID, apply a
        hashing algorithm to the ID, and return the hashed value.

        :return: A hashed version of the RFID tag's ID, or None if no tag was scanned.
        """
        pass