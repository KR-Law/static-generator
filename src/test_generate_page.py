import unittest

from generate_page import extract_title

class TestMarkdownToHTML(unittest.TestCase):
    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        title = extract_title(md)
        self.assertEqual("this is an h1", title)

    def test_extract_title_missing(self):
        md = "## Sub\nParagraph"
        with self.assertRaises(Exception):
            extract_title(md)
    
    def test_extract_title_leading_space(self):
        md = "   # Title\nText"
        self.assertEqual("Title", extract_title(md))

    def test_extract_title_empty_h1(self):
        md = "#   \nBody"
        with self.assertRaises(Exception) as cm:
            extract_title(md)
        self.assertIn("h1 title is empty", str(cm.exception))
    
    def test_extract_title_not_h1(self):
        md = "## Not h1"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_returns_first_valid_h1(self):
        md = """
   # First Title
paragraph

# Second Title
## Third
"""
        self.assertEqual("First Title", extract_title(md))