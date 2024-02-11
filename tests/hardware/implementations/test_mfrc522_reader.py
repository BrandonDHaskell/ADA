import unittest
import sys
from unittest.mock import Mock, patch, MagicMock

# Mock RPi.GPIO module
sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = MagicMock()
sys.modules['mfrc522'] = MagicMock()

from src.hardware.implementations.mfrc522_reader import MFRC522Reader



class TestMFRC522Reader(unittest.TestCase):
    def setUp(self):
        self.config = {
            "name": "TestRFIDReader",
            "hmac_secret_key": "test_secret_key"    #HMAC test case
        }
        self.rfid_reader = MFRC522Reader(self.config)

        # Mocking the SimpleMFRC522 reader and GPIO
        self.rfid_reader.reader = Mock()
        self.rfid_reader.reader.read_id_no_block = Mock()

    @patch("src.hardware.implementations.mfrc522_reader.hmac.new")
    def test_scan_for_obf_id(self, mock_hmac_new):

        # Setup the mock for hmac
        mock_hmac_obj = Mock()
        mock_hmac_new.return_value = mock_hmac_obj
        mock_hmac_obj.hexdigest.return_value = "hex_hashed_id"

        # Simulate a successful RFID scan
        self.rfid_reader.reader.read_id_no_block.return_value = 123456789
        hashed_id = self.rfid_reader.scan_for_obf_id()

        mock_hmac_new.assert_called_once_with(
            self.config["hmac_secret_key"].encode("utf-8"),
            msg=str(123456789).encode("utf-8"), 
            digestmod="sha256"
        )
        mock_hmac_obj.hexdigest.assert_called_once()
        self.assertEqual(hashed_id, 'hex_hashed_id')

    def test_scan_for_obf_id_no_card(self):
        # Simulate no RFID card being scanned
        self.rfid_reader.reader.read_id_no_block.return_value = None
        result = self.rfid_reader.scan_for_obf_id()

        # Assertions
        self.assertIsNone(result, "Should return None when no card is scanned")

    # Additional tests can be added here to further verify the behavior of MFRC522Reader

if __name__ == '__main__':
    unittest.main()
