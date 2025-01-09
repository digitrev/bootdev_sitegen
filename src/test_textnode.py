"""Test the TextNode class"""

import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    """TestTextNode - tests the TextNode functionality"""

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "a url")
        node2 = TextNode("This is a text node", TextType.ITALIC, "a url")
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        node = TextNode("This is a text node with different data", TextType.ITALIC, "a url")
        node2 = TextNode("This is a text node", TextType.ITALIC, "a url")
        self.assertNotEqual(node, node2)

    def test_not_eq_different_type(self):
        node = TextNode("This is a text node", TextType.ITALIC, "a url")
        node2 = TextNode("This is a text node", TextType.BOLD, "a url")
        self.assertNotEqual(node, node2)

    def test_not_eq_url_v_no_url(self):
        node = TextNode("This is a text node", TextType.ITALIC, "a url")
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
