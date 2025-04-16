import unittest
from main import extract_title

class TestMain(unittest.TestCase):
    def test_extract_title(self):
        self.assertEqual(extract_title("# Title"), "Title")

    def test_extract_title_no_title(self):
        with self.assertRaises(Exception):
            extract_title("No title here")

    def test_extract_title_empty(self):
        with self.assertRaises(Exception):
            extract_title("")

    def test_extract_title_multiple_lines(self):
        self.assertEqual(extract_title("# Title\n## Subtitle"), "Title")

    def test_extract_title_multiple_hashes(self):
        with self.assertRaises(Exception):
            extract_title("### Title")