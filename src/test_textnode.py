"""Test the TextNode class"""

import unittest
from htmlnode import HTMLNode
from textnode import (
    TextNode,
    TextType,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_links,
    split_nodes_delimiter,
    swap_types,
    text_to_textnodes,
)


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
        node = TextNode(
            "This is a text node with different data", TextType.ITALIC, "a url"
        )
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
        self.assertEqual(repr(node), "TextNode(Text node, bold, https://google.ca)")

    def test_repr_no_url(self):
        """Test self representation without url"""
        node = TextNode("Text node", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(Text node, bold, None)")

    def test_html_conversion_normal(self):
        """Test text_node_to_html_node(), no decoration"""
        node = TextNode("Text node", TextType.NORMAL)
        self.assertEqual(
            node.text_node_to_html_node(), HTMLNode(None, "Text node", None, None)
        )

    def test_html_conversion_tagged(self):
        """Test text_node_to_html_node(), basic tag"""
        node = TextNode("Text node", TextType.CODE)
        self.assertEqual(
            node.text_node_to_html_node(), HTMLNode("code", "Text node", None, None)
        )

    def test_html_conversion_link(self):
        """Test text_node_to_html_node(), link"""
        node = TextNode("Text node", TextType.LINK, "google.ca")
        self.assertEqual(
            node.text_node_to_html_node(),
            HTMLNode("a", "Text node", None, {"href": "google.ca"}),
        )

    def test_html_conversion_image(self):
        """Test text_node_to_html_node(), image"""
        node = TextNode("Text node", TextType.IMAGE, "google.ca/test.png")
        self.assertEqual(
            node.text_node_to_html_node(),
            HTMLNode("img", props={"src": "google.ca/test.png", "alt": "Text node"}),
        )


class TestTextFunctions(unittest.TestCase):
    """Tests text node related functions"""

    def test_swap_types_1_2(self):
        """Test swap_types from 1 to 2"""
        text_type = swap_types(TextType.BOLD, TextType.BOLD, TextType.NORMAL)
        self.assertEqual(text_type, TextType.NORMAL)

    def test_swap_types_2_1(self):
        """Test swap_types from 2 to 1"""
        text_type = swap_types(TextType.NORMAL, TextType.BOLD, TextType.NORMAL)
        self.assertEqual(text_type, TextType.BOLD)

    def test_swap_types_error(self):
        """Test swap_types with bad data"""
        with self.assertRaises(ValueError) as ve:
            swap_types(TextType.ITALIC, TextType.BOLD, TextType.NORMAL)
        self.assertEqual(
            str(ve.exception), "to_change should be one of type_one or type_two"
        )

    def test_split_nodes_single(self):
        """Test split_nodes_delimiter with one input text"""
        node = TextNode("Simple *bold* text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Simple ", TextType.NORMAL),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.NORMAL),
            ],
        )

    def test_split_nodes_two_delimiters(self):
        """Test split_nodes_delimiter with one input text, two delimiters"""
        node = TextNode("Simple *bold* text with followup *bold*", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Simple ", TextType.NORMAL),
                TextNode("bold", TextType.BOLD),
                TextNode(" text with followup ", TextType.NORMAL),
                TextNode("bold", TextType.BOLD),
            ],
        )

    def test_split_nodes_two_nodes(self):
        """Test split_nodes_delimiter with one input text, two delimiters"""
        node = TextNode("Simple *bold* text with followup *bold*", TextType.NORMAL)
        node2 = TextNode("Testing *bold* text", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node, node2], "*", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Simple ", TextType.NORMAL),
                TextNode("bold", TextType.BOLD),
                TextNode(" text with followup ", TextType.NORMAL),
                TextNode("bold", TextType.BOLD),
                TextNode("Testing ", TextType.NORMAL),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.NORMAL),
            ],
        )

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
            [("alt", "example.com/test.gif")],
        )

    def test_extract_markdown_images_double(self):
        """Test extract_markdown_images, two images"""
        self.assertEqual(
            extract_markdown_images(
                "Text ![alt](example.com/test.gif) more ![alt2](t.co/other.png)"
            ),
            [("alt", "example.com/test.gif"), ("alt2", "t.co/other.png")],
        )

    def test_extract_markdown_images_no_image(self):
        """Test extract_markdown_images, no images"""
        self.assertEqual(extract_markdown_images("Text"), [])

    def test_extract_markdown_links_single(self):
        """Test extract_markdown_links, single link"""
        self.assertEqual(
            extract_markdown_links("Text [link](example.com)"),
            [("link", "example.com")],
        )

    def test_extract_markdown_links_double(self):
        """Test extract_markdown_links, two links"""
        self.assertEqual(
            extract_markdown_links(
                "Text ![link](example.com) more ![link2](google.ca)"
            ),
            [("link", "example.com"), ("link2", "google.ca")],
        )

    def test_extract_markdown_links_no_image(self):
        """Test extract_markdown_links, no links"""
        self.assertEqual(extract_markdown_links("Text"), [])

    def test_split_nodes_image_single(self):
        """Test split_nodes_image with a single image"""
        node = TextNode("Pre text ![alt text](example.com/image.png)", TextType.NORMAL)
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("Pre text ", TextType.NORMAL),
                TextNode("alt text", TextType.IMAGE, "example.com/image.png"),
            ],
        )

    def test_split_nodes_image_double(self):
        """Test split_nodes_image with two images"""
        node = TextNode(
            "Pre text ![alt text](example.com/image.png) mid text "
            + "![other alt text](example.com/img.jpg) post text",
            TextType.NORMAL,
        )
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("Pre text ", TextType.NORMAL),
                TextNode("alt text", TextType.IMAGE, "example.com/image.png"),
                TextNode(" mid text ", TextType.NORMAL),
                TextNode("other alt text", TextType.IMAGE, "example.com/img.jpg"),
                TextNode(" post text", TextType.NORMAL),
            ],
        )

    def test_split_nodes_image_double_node(self):
        """Test split_nodes_image with two images, one per node"""
        node = TextNode(
            "Pre text ![alt text](example.com/image.png) mid text ",
            TextType.NORMAL,
        )
        node2 = TextNode(
            "![other alt text](example.com/img.jpg) post text",
            TextType.NORMAL,
        )
        self.assertEqual(
            split_nodes_image([node, node2]),
            [
                TextNode("Pre text ", TextType.NORMAL),
                TextNode("alt text", TextType.IMAGE, "example.com/image.png"),
                TextNode(" mid text ", TextType.NORMAL),
                TextNode("other alt text", TextType.IMAGE, "example.com/img.jpg"),
                TextNode(" post text", TextType.NORMAL),
            ],
        )

    def test_split_nodes_link_single(self):
        """Test split_nodes_link with a single link"""
        node = TextNode("Pre text [link text](example.com)", TextType.NORMAL)
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("Pre text ", TextType.NORMAL),
                TextNode("link text", TextType.LINK, "example.com"),
            ],
        )

    def test_split_nodes_link_double(self):
        """Test split_nodes_link with two links"""
        node = TextNode(
            "Pre text [link text](example.com) mid text "
            + "[other link text](google.ca) post text",
            TextType.NORMAL,
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("Pre text ", TextType.NORMAL),
                TextNode("link text", TextType.LINK, "example.com"),
                TextNode(" mid text ", TextType.NORMAL),
                TextNode("other link text", TextType.LINK, "google.ca"),
                TextNode(" post text", TextType.NORMAL),
            ],
        )

    def test_split_nodes_link_double_node(self):
        """Test split_nodes_link with two links, one per node"""
        node = TextNode(
            "Pre text [link text](example.com) mid text ",
            TextType.NORMAL,
        )
        node2 = TextNode(
            "[other link text](google.ca) post text",
            TextType.NORMAL,
        )
        self.assertEqual(
            split_nodes_link([node, node2]),
            [
                TextNode("Pre text ", TextType.NORMAL),
                TextNode("link text", TextType.LINK, "example.com"),
                TextNode(" mid text ", TextType.NORMAL),
                TextNode("other link text", TextType.LINK, "google.ca"),
                TextNode(" post text", TextType.NORMAL),
            ],
        )

    def test_text_to_textnodes_plain(self):
        """Test text_to_textnodes, plain text"""
        self.assertEqual(
            text_to_textnodes("Plain text"), [TextNode("Plain text", TextType.NORMAL)]
        )

    def test_text_to_textnodes_bold(self):
        """Test text_to_textnodes, bold text"""
        self.assertEqual(
            text_to_textnodes("**Bold** text"),
            [TextNode("Bold", TextType.BOLD), TextNode(" text", TextType.NORMAL)],
        )

    def test_text_to_textnodes_italic(self):
        """Test text_to_textnodes, italic text"""
        self.assertEqual(
            text_to_textnodes("*Italic* text"),
            [TextNode("Italic", TextType.ITALIC), TextNode(" text", TextType.NORMAL)],
        )

    def test_text_to_textnodes_code(self):
        """Test text_to_textnodes, code text"""
        self.assertEqual(
            text_to_textnodes("`Code` text"),
            [TextNode("Code", TextType.CODE), TextNode(" text", TextType.NORMAL)],
        )

    def test_text_to_textnodes_link(self):
        """Test text_to_textnodes, link"""
        self.assertEqual(
            text_to_textnodes("Link to [google](google.ca) with trail"),
            [
                TextNode("Link to ", TextType.NORMAL),
                TextNode("google", TextType.LINK, "google.ca"),
                TextNode(" with trail", TextType.NORMAL),
            ],
        )

    def test_text_to_textnodes_image(self):
        """Test text_to_textnodes, image"""
        self.assertEqual(
            text_to_textnodes(
                "Image for ![fake thing](example.com/test.png) with trail"
            ),
            [
                TextNode("Image for ", TextType.NORMAL),
                TextNode("fake thing", TextType.IMAGE, "example.com/test.png"),
                TextNode(" with trail", TextType.NORMAL),
            ],
        )

    def test_text_to_textnodes_everything(self):
        """Test text_to_textnodes, all at once"""
        self.assertEqual(
            text_to_textnodes(
                "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
            ),
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.NORMAL),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
