"""Test the TextNode class"""

import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    """TestTextNode - tests the TextNode functionality"""

    def test_eq(self):
        """Test equality of text node without URL"""
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        """Test equality of text node with URL"""
        node = TextNode("This is a text node", TextType.ITALIC, "a url")
        node2 = TextNode("This is a text node", TextType.ITALIC, "a url")
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        """Test non-equality of Text Node where text differs"""
        node = TextNode("This is a text node with different data", TextType.ITALIC, "a url")
        node2 = TextNode("This is a text node", TextType.ITALIC, "a url")
        self.assertNotEqual(node, node2)

    def test_not_eq_different_type(self):
        """Test non-equality of Text Node where text type differs"""
        node = TextNode("This is a text node", TextType.ITALIC, "a url")
        node2 = TextNode("This is a text node", TextType.BOLD, "a url")
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        """Test non-equality of Text Node where URL differs"""
        node = TextNode("This is a text node", TextType.NORMAL, "basic url")
        node2 = TextNode("This is a text node", TextType.NORMAL, "different url")
        self.assertNotEqual(node, node2)

    def test_not_eq_url_v_no_url(self):
        """Test non-equality of Text Node where URL is missing in one"""
        node = TextNode("This is a text node", TextType.ITALIC, "a url")
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_repr_with_url(self):
        """Test Text Node representation"""
        node = TextNode("Text node", TextType.BOLD, "https://google.ca")
        self.assertEqual(repr(node),
                         "TextNode(Text node, bold, https://google.ca)")

    def test_repr_no_url(self):
        """Test Text Node representation"""
        node = TextNode("Text node", TextType.BOLD)
        self.assertEqual(repr(node),
                         "TextNode(Text node, bold, None)")

    def test_html_conversion_normal(self):
        """Test TextNode.text_node_to_html_node(), no decoration"""
        node = TextNode("Text node", TextType.NORMAL)
        self.assertEqual(repr(node.text_node_to_html_node()),
                         "HTMLNode(None, Text node, None, None)")

    def test_html_conversion_tagged(self):
        """Test TextNode.text_node_to_html_node(), basic tag"""
        node = TextNode("Text node", TextType.CODE)
        self.assertEqual(repr(node.text_node_to_html_node()),
                         "HTMLNode(code, Text node, None, None)")

    def test_html_conversion_link(self):
        """Test TextNode.text_node_to_html_node(), link"""
        node = TextNode("Text node", TextType.LINK, "google.ca")
        self.assertEqual(repr(node.text_node_to_html_node()),
                         "HTMLNode(a, Text node, None, {'href': 'google.ca'})")

    def test_html_conversion_image(self):
        """Test TextNode.text_node_to_html_node(), image"""
        node = TextNode("Text node", TextType.IMAGE, "google.ca/test.png")
        self.assertEqual(repr(node.text_node_to_html_node()),
                         "HTMLNode(img, , None, {'src': 'google.ca/test.png', 'alt': 'Text node'})")


if __name__ == "__main__":
    unittest.main()
