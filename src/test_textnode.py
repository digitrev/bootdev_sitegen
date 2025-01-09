"""Test the TextNode class"""

import unittest
from textnode import TextNode, TextType, extract_markdown_images, extract_markdown_links, split_nodes_delimiter

class TestTextNode(unittest.TestCase):
    """TestTextNode - tests the TextNode functionality"""

    def test_eq(self):
        """Test equality without URL"""
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        """Test equality with URL"""
        node = TextNode("This is a text node", TextType.ITALIC, "a url")
        node2 = TextNode("This is a text node", TextType.ITALIC, "a url")
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        """Test non-equality where text differs"""
        node = TextNode("This is a text node with different data", TextType.ITALIC, "a url")
        node2 = TextNode("This is a text node", TextType.ITALIC, "a url")
        self.assertNotEqual(node, node2)

    def test_not_eq_different_type(self):
        """Test non-equality where text type differs"""
        node = TextNode("This is a text node", TextType.ITALIC, "a url")
        node2 = TextNode("This is a text node", TextType.BOLD, "a url")
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        """Test non-equality where URL differs"""
        node = TextNode("This is a text node", TextType.NORMAL, "basic url")
        node2 = TextNode("This is a text node", TextType.NORMAL, "different url")
        self.assertNotEqual(node, node2)

    def test_not_eq_url_v_no_url(self):
        """Test non-equality where URL is missing in one"""
        node = TextNode("This is a text node", TextType.ITALIC, "a url")
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_repr_with_url(self):
        """Test self representation"""
        node = TextNode("Text node", TextType.BOLD, "https://google.ca")
        self.assertEqual(repr(node),
                         "TextNode(Text node, bold, https://google.ca)")

    def test_repr_no_url(self):
        """Test self representation without url"""
        node = TextNode("Text node", TextType.BOLD)
        self.assertEqual(repr(node),
                         "TextNode(Text node, bold, None)")

    def test_html_conversion_normal(self):
        """Test text_node_to_html_node(), no decoration"""
        node = TextNode("Text node", TextType.NORMAL)
        self.assertEqual(repr(node.text_node_to_html_node()),
                         "HTMLNode(None, Text node, None, None)")

    def test_html_conversion_tagged(self):
        """Test text_node_to_html_node(), basic tag"""
        node = TextNode("Text node", TextType.CODE)
        self.assertEqual(repr(node.text_node_to_html_node()),
                         "HTMLNode(code, Text node, None, None)")

    def test_html_conversion_link(self):
        """Test text_node_to_html_node(), link"""
        node = TextNode("Text node", TextType.LINK, "google.ca")
        self.assertEqual(repr(node.text_node_to_html_node()),
                         "HTMLNode(a, Text node, None, {'href': 'google.ca'})")

    def test_html_conversion_image(self):
        """Test text_node_to_html_node(), image"""
        node = TextNode("Text node", TextType.IMAGE, "google.ca/test.png")
        self.assertEqual(repr(node.text_node_to_html_node()),
                         "HTMLNode(img, , None, {'src': 'google.ca/test.png', 'alt': 'Text node'})")

class TestTextFunctions(unittest.TestCase):
    """Tests text node related functions"""
    def test_split_nodes_single(self):
        """Test split_nodes_delimiter with one input text"""
        node = TextNode("Simple *bold* text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        output = "[TextNode(Simple , normal, None),"
        output += " TextNode(bold, bold, None), TextNode( text, normal, None)]"
        self.assertEqual(repr(new_nodes),
                         output)

    def test_split_nodes_two_delimiters(self):
        """Test split_nodes_delimiter with one input text, two delimiters"""
        node = TextNode("Simple *bold* text with followup *bold*", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        output = "[TextNode(Simple , normal, None), TextNode(bold, bold, None),"
        output += " TextNode( text with followup , normal, None)"
        output += ", TextNode(bold, bold, None), TextNode(, normal, None)]"
        self.assertEqual(repr(new_nodes),
                         output)

    def test_split_nodes_two_nodes(self):
        """Test split_nodes_delimiter with one input text, two delimiters"""
        node = TextNode("Simple *bold* text with followup *bold*", TextType.NORMAL)
        node2 = TextNode("Testing *bold* text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node, node2], "*", TextType.BOLD)
        output = "[TextNode(Simple , normal, None), TextNode(bold, bold, None),"
        output += " TextNode( text with followup , normal, None), TextNode(bold, bold, None)"
        output += ", TextNode(, normal, None), TextNode(Testing , normal, None), "
        output += "TextNode(bold, bold, None), TextNode( text, normal, None)]"
        self.assertEqual(repr(new_nodes),
                         output)

    def test_split_nodes_non_normal(self):
        """Test split_nodes_delimiter when the text is not NORMAL"""
        node = TextNode("Already bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(repr(new_nodes), "[TextNode(Already bold, bold, None)]")

    def test_split_nodes_unpaired_delimiter(self):
        """Test split_nodes_delimiter when there's an unclosed delimiter"""
        node = TextNode("Only one *in this", TextType.NORMAL)
        with self.assertRaises(ValueError) as ve:
            split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(str(ve.exception), "Missing delimiter")

    def test_extract_markdown_images_single(self):
        """Test extract_markdown_images, single image"""
        self.assertEqual(
            extract_markdown_images("Text ![alt](example.com/test.gif)"),
            [("alt", "example.com/test.gif")])

    def test_extract_markdown_images_double(self):
        """Test extract_markdown_images, two images"""
        self.assertEqual(
            extract_markdown_images(
                "Text ![alt](example.com/test.gif) more ![alt2](t.co/other.png)"),
                [("alt", "example.com/test.gif"), ("alt2", "t.co/other.png")])

    def test_extract_markdown_images_no_image(self):
        """Test extract_markdown_images, no images"""
        self.assertEqual(extract_markdown_images("Text"),[])

    def test_extract_markdown_links_single(self):
        """Test extract_markdown_links, single link"""
        self.assertEqual(
            extract_markdown_links("Text [link](example.com)"),
            [("link", "example.com")])

    def test_extract_markdown_links_double(self):
        """Test extract_markdown_links, two links"""
        self.assertEqual(
            extract_markdown_links(
                "Text ![link](example.com) more ![link2](google.ca)"),
                [("link", "example.com"), ("link2", "google.ca")])

    def test_extract_markdown_links_no_image(self):
        """Test extract_markdown_links, no links"""
        self.assertEqual(extract_markdown_links("Text"),[])

if __name__ == "__main__":
    unittest.main()
