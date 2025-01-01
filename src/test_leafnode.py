import unittest

from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_no_tag(self):
        node = LeafNode(None, "test")
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, "test")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props_to_html(), "")
        self.assertEqual(node.to_html(), "test")

    def test_with_tag(self):
        node = LeafNode("p", "paragraph")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "paragraph")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props_to_html(), "")
        self.assertEqual(node.to_html(), "<p>paragraph</p>")

    def test_with_props(self):
        node = LeafNode("a", "link", {"href": "google.ca"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "link")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props_to_html(), ' href="google.ca"')
        self.assertEqual(node.to_html(), '<a href="google.ca">link</a>')


if __name__ == "__main__":
    unittest.main()