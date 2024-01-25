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
            "name": "TestRFIDReader"
        }
        self.rfid_reader = MFRC522Reader(self.config)

        # Mocking the SimpleMFRC522 reader and GPIO
        self.rfid_reader.reader = Mock()
        self.rfid_reader.reader.read_id_no_block = Mock()

    @patch('src.hardware.implementations.mfrc522_reader.base64.b64encode')
    @patch('src.hardware.implementations.mfrc522_reader.hashlib.sha256')
    def test_scan_for_obf_id(self, mock_sha256, mock_b64encode):
        # Setup the mock for hashlib and base64
        mock_hash_obj = Mock()
        mock_sha256.return_value = mock_hash_obj
        mock_hash_obj.digest.return_value = b'hashed_id_bytes'
        mock_b64encode.return_value = b'base64_hashed_id'

        # Simulate a successful RFID scan
        self.rfid_reader.reader.read_id_no_block.return_value = 123456789
        hashed_id = self.rfid_reader.scan_for_obf_id()

        # Assertions
        mock_sha256.assert_called_once()
        mock_hash_obj.update.assert_called_once_with(b'123456789')
        mock_b64encode.assert_called_once_with(b'hashed_id_bytes')
        self.assertEqual(hashed_id, 'base64_hashed_id')

    def test_scan_for_obf_id_no_card(self):
        # Simulate no RFID card being scanned
        self.rfid_reader.reader.read_id_no_block.return_value = None
        result = self.rfid_reader.scan_for_obf_id()

        # Assertions
        self.assertIsNone(result, "Should return None when no card is scanned")

    # Additional tests can be added here to further verify the behavior of MFRC522Reader

if __name__ == '__main__':
    unittest.main()
