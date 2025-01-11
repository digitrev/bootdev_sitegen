"""testing main functions"""

import unittest

from main import extract_title


class TestMain(unittest.TestCase):
    """Test Main"""

    def test_extract_title_simple(self):
        """Test extract_title() on basic text"""
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_extract_title_multiline(self):
        """Test extract_title() on multiline text"""
        self.assertEqual(extract_title("# Hello\n\nSome other stuff"), "Hello")

    def test_extract_title_no_h1(self):
        """Test extract_title() on multiline text"""
        with self.assertRaises(ValueError) as ve:
            extract_title("Hello\n\nSome other stuff")
        self.assertEqual(str(ve.exception), "Markdown requires h1 tag")

    def test_extract_title_delayed_header(self):
        """Test extract_title() on multiline text"""
        self.assertEqual(extract_title("Some other stuff\n\n# Delayed"), "Delayed")

if __name__ == "__main__":
    unittest.main()
