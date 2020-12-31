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

VALID_FILE_SHOPPING_DICT = {
    "BEVG": ["GJHGTFBNGDVZJGDIPXVS", "IHDCZIPWLZJLPDSGNEAH"],
    "CANF": ["OUXSCGSYBHQYHNMDQOBL"],
    "FRZN": ["SCHIMIXOUHNAWLXRZEPT"],
}

VALID_FILE_SHOPPING_LEAPYEAR_DICT = {"BEVG": ["IHDCZIPWLZJLPDSGNEAH"]}

VALID_FILE_SUBTYPES_LEAPYEAR_LIST = ["ZYUFGN"]

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
    def test_process_file(self, filename="any_string", productcode=None):
        # Test correct input file
        mocked_open_valid = mock.mock_open(read_data=VALID_FILE)
        with mock.patch("builtins.open", mocked_open_valid):
            with open("any_string") as f:
                name, date, shopping, subtypes = process.process_file(f, None)
                self.assertEqual(name, "Jamie")
                self.assertEqual(date, datetime.date(2020, 1, 23))
                self.assertEqual(shopping, VALID_FILE_SHOPPING_DICT)
                self.assertEqual(subtypes, [])

        # Test correct input file (with a leap year)
        mocked_open_leapyear = mock.mock_open(read_data=VALID_FILE_LEAPYEAR)
        with mock.patch("builtins.open", mocked_open_leapyear):
            with open("any_string") as f:
                name, date, shopping, subtypes = process.process_file(f, "BEVG")
                self.assertEqual(name, "Jamie")
                self.assertEqual(date, datetime.date(2020, 2, 29))
                self.assertEqual(shopping, VALID_FILE_SHOPPING_LEAPYEAR_DICT)
                self.assertEqual(subtypes, VALID_FILE_SUBTYPES_LEAPYEAR_LIST)

        # Test incorrect date in file
        mocked_open_invalid_date = mock.mock_open(read_data=INVALID_DATE)
        with mock.patch("builtins.open", mocked_open_invalid_date):
            with open("any_string") as f:
                self.assertRaises(ValueError, process.process_file, f, None)

        # Test incorrect barcode in file
        mocked_open_invalid_barcode = mock.mock_open(read_data=INVALID_BARCODE)
        with mock.patch("builtins.open", mocked_open_invalid_barcode):
            with open("any_string") as f:
                self.assertRaises(ValueError, process.process_file, f, None)

    def test_parse_line(self, line="CANFDNSKAVOUXSCGSYBHQYHNMDQOBL"):
        # Test valid line
        code, subtype, id = process.parse_line(line)
        self.assertEqual(code, "CANF")
        self.assertEqual(subtype, "DNSKAV")
        self.assertEqual(id, "OUXSCGSYBHQYHNMDQOBL")

        # Test incorrect peoduct code in line
        self.assertRaises(ValueError, process.parse_line, "CAXFDNSK")

    def test_count_shopping(self, shopping=VALID_FILE_SHOPPING_DICT):
        # Test counting over shopping dict
        count, max = process.count_shopping(shopping)
        self.assertEqual(count, 4)
        self.assertEqual(max, 2)
