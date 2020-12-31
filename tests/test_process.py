#!/usr/bin/python3

import datetime
import tempfile
import unittest

import mock

from processor import process

VALID_FILE = (
    "01232020Jamie\n"
    "BEVGTTKYGDGJHGTFBNGDVZJGDIPXVS\n"
    "CANFDNSKAVOUXSCGSYBHQYHNMDQOBL\n"
    "FRZNQQNPSESCHIMIXOUHNAWLXRZEPT\n"
    "BEVGZYUFGNIHDCZIPWLZJLPDSGNEAH"
)

VALID_FILE_LEAPYEAR = "02292020Jamie\nBEVGZYUFGNIHDCZIPWLZJLPDSGNEAH"

INVALID_DATE = "01332020Jamie\nBEVGZYUFGNIHDCZIPWLZJLPDSGNEAH"

INVALID_BARCODE = (
    "01232020Jamie\nCANFDNOUXSCGSYBHQYHNMDQOBL\nBEVGZYUFGNIHDCZIPWLZJLPDSGNEAH"
)


class TestProcess(unittest.TestCase):
    def test_get_path(self):
        # Test function returning a valid path if the file exists, or
        # raising an error otherwise.
        with tempfile.NamedTemporaryFile() as f:
            filename = f.name

            # Test get_path with existing and valid file
            path_exists = process.get_path(filename)
            self.assertEqual(filename, path_exists.as_posix())

        # Test get_path with incorrect filename
        self.assertRaises(FileNotFoundError, process.get_path, "no_exist.txt")

    # Filename is not used; file content is mocked to test different scenarios
    def test_process_file(self, filename="any_string"):
        # Test correct input file
        mocked_open_valid = mock.mock_open(read_data=VALID_FILE)
        with mock.patch("builtins.open", mocked_open_valid):
            with open("any_string") as f:
                name, date, count = process.process_file(f)
                self.assertEqual(name, "Jamie")
                self.assertEqual(date, datetime.date(2020, 1, 23))
                self.assertEqual(count, 4)

        # Test correct input file (with a leap year)
        mocked_open_leapyear = mock.mock_open(read_data=VALID_FILE_LEAPYEAR)
        with mock.patch("builtins.open", mocked_open_leapyear):
            with open("any_string") as f:
                name, date, count = process.process_file(f)
                self.assertEqual(name, "Jamie")
                self.assertEqual(date, datetime.date(2020, 2, 29))
                self.assertEqual(count, 1)

        # Test incorrect date in file
        mocked_open_invalid_date = mock.mock_open(read_data=INVALID_DATE)
        with mock.patch("builtins.open", mocked_open_invalid_date):
            with open("any_string") as f:
                self.assertRaises(ValueError, process.process_file, f)

        # Test incorrect barcode in file
        mocked_open_invalid_barcode = mock.mock_open(read_data=INVALID_BARCODE)
        with mock.patch("builtins.open", mocked_open_invalid_barcode):
            with open("any_string") as f:
                self.assertRaises(ValueError, process.process_file, f)
