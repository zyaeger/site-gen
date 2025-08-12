import unittest

from src.page_gen import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = "# Header1"
        title = extract_title(md)
        expected = "Header1"
        self.assertEqual(expected, title)

    def test_extract_title_blocks(self):
        md = """
This is a paragraph

## This is wrong header
# This is correct header
"""
        title = extract_title(md)
        expected = "This is correct header"
        self.assertEqual(title, expected)

    def test_extract_title_no_header(self):
        md = """
This is text that has no header

foo
"""
        with self.assertRaises(ValueError):
            extract_title(md)


if __name__ == "__main__":
    unittest.main()
