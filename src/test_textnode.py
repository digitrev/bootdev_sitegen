"""Test the TextNode class"""

import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import (
    BlockType,
    TextNode,
    TextType,
    block_to_block_type,
    block_type_to_helper_function,
    code_to_html_node,
    extract_markdown_images,
    heading_to_html_node,
    markdown_to_blocks,
    ordered_list_to_html_node,
    paragraph_to_html_node,
    quote_to_html_node,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_links,
    split_nodes_delimiter,
    swap_types,
    text_to_textnodes,
    unordered_list_to_html_node,
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
        self.assertEqual(node.to_html_node(), HTMLNode(None, "Text node", None, None))

    def test_html_conversion_tagged(self):
        """Test text_node_to_html_node(), basic tag"""
        node = TextNode("Text node", TextType.CODE)
        self.assertEqual(node.to_html_node(), HTMLNode("code", "Text node", None, None))

    def test_html_conversion_link(self):
        """Test text_node_to_html_node(), link"""
        node = TextNode("Text node", TextType.LINK, "google.ca")
        self.assertEqual(
            node.to_html_node(),
            HTMLNode("a", "Text node", None, {"href": "google.ca"}),
        )

    def test_html_conversion_image(self):
        """Test text_node_to_html_node(), image"""
        node = TextNode("Text node", TextType.IMAGE, "google.ca/test.png")
        self.assertEqual(
            node.to_html_node(),
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

    def test_markdown_to_blocks_single(self):
        """Test markdown_to_blocks() on a single line string"""
        self.assertEqual(markdown_to_blocks("Simple text"), ["Simple text"])

    def test_markdown_to_blocks_single_one_newline(self):
        """Test markdown_to_blocks() with one newline"""
        self.assertEqual(
            markdown_to_blocks("Simple text\nBreak"), ["Simple text\nBreak"]
        )

    def test_markdown_to_blocks_single_leading_whitespace(self):
        """Test markdown_to_blocks() with leading whitespace"""
        self.assertEqual(markdown_to_blocks("\t \nSimple text"), ["Simple text"])

    def test_markdown_to_blocks_single_trailing_whitespace(self):
        """Test markdown_to_blocks() with trailing whitespace"""
        self.assertEqual(markdown_to_blocks("Simple text\n \t"), ["Simple text"])

    def test_markdown_to_blocks_multiple(self):
        """Test markdown_to_blocks() with three blocks"""
        self.assertEqual(
            markdown_to_blocks("Block one\n\nBlock two\n\nBlock three"),
            ["Block one", "Block two", "Block three"],
        )

    def test_markdown_to_blocks_multiple_extra_newline(self):
        """Test markdown_to_blocks() with two blocks and an extra newline"""
        self.assertEqual(
            markdown_to_blocks("Block one\n\n\nBlock two"),
            ["Block one", "Block two"],
        )

    def test_markdown_to_blocks_multiple_extra_newlines(self):
        """Test markdown_to_blocks() with four newlines"""
        self.assertEqual(
            markdown_to_blocks("Block one\n\n\n\nBlock two"),
            ["Block one", "Block two"],
        )

    def test_block_to_block_type_headings(self):
        """Test block_to_block_type() with headings"""
        for n in range(6):
            self.assertEqual(
                block_to_block_type(f"{'#'*(n+1)} some text"), BlockType.HEADING
            )

    def test_block_to_block_type_code(self):
        """Test block_to_block_type() with code block"""
        self.assertEqual(block_to_block_type("```some code```"), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        """Test block_to_block_type() with quote block"""
        self.assertEqual(block_to_block_type(">line 1\n>line 2"), BlockType.QUOTE)

    def test_block_to_block_type_ordered_list(self):
        """Test block_to_block_type() with ordered list block"""
        self.assertEqual(
            block_to_block_type("1. line 1\n2. line 2"), BlockType.ORDERED_LIST
        )

    def test_block_to_block_type_unordered_list(self):
        """Test block_to_block_type() with unordered list block"""
        self.assertEqual(
            block_to_block_type("* line 1\n- line 2"), BlockType.UNORDERED_LIST
        )

    def test_block_to_block_type_paragraph(self):
        """Test block_to_block_type() with paragraph block"""
        self.assertEqual(block_to_block_type("just some text"), BlockType.PARAGRAPH)

    def test_block_to_block_type_header_without_space(self):
        """Test block_to_block_type() with a header without the space"""
        self.assertEqual(block_to_block_type("###bad header"), BlockType.PARAGRAPH)

    def test_block_to_block_type_header_seven(self):
        """Test block_to_block_type() with seven leading #"""
        self.assertEqual(block_to_block_type("####### bad header"), BlockType.PARAGRAPH)

    def test_block_to_block_type_code_no_leading(self):
        """Test block_to_block_type() with no leading backticks"""
        self.assertEqual(block_to_block_type("code block```"), BlockType.PARAGRAPH)

    def test_block_to_block_type_code_no_trailing(self):
        """Test block_to_block_type() with no trailing backticks"""
        self.assertEqual(block_to_block_type("```code block"), BlockType.PARAGRAPH)

    def test_block_to_block_type_mixed_quote(self):
        """Test block_to_block_type() with mixed quote and non-quote"""
        self.assertEqual(
            block_to_block_type(">line one\nline two"), BlockType.PARAGRAPH
        )

    def test_block_to_block_type_mixed_ordered(self):
        """Test block_to_block_type() with mixed ordered and non-ordered"""
        self.assertEqual(
            block_to_block_type("1. line one\nline two"), BlockType.PARAGRAPH
        )

    def test_block_to_block_type_incorrect_ordered(self):
        """Test block_to_block_type() with incorrect ordering"""
        self.assertEqual(
            block_to_block_type("2. line one\n1. line two"), BlockType.PARAGRAPH
        )

    def test_block_to_block_type_mixed_unordered(self):
        """Test block_to_block_type() with mixed unordered and non-unordered"""
        self.assertEqual(
            block_to_block_type("* line one\nline two"), BlockType.PARAGRAPH
        )

    def test_block_type_to_helper_function_paragraph(self):
        """Test block_type_to_helper_function for paragraph"""
        self.assertEqual(
            block_type_to_helper_function(BlockType.PARAGRAPH), paragraph_to_html_node
        )

    def test_block_type_to_helper_function_heading(self):
        """Test block_type_to_helper_function for heading"""
        self.assertEqual(
            block_type_to_helper_function(BlockType.HEADING), heading_to_html_node
        )

    def test_block_type_to_helper_function_code(self):
        """Test block_type_to_helper_function for code"""
        self.assertEqual(
            block_type_to_helper_function(BlockType.CODE), code_to_html_node
        )

    def test_block_type_to_helper_function_quote(self):
        """Test block_type_to_helper_function for quote"""
        self.assertEqual(
            block_type_to_helper_function(BlockType.QUOTE), quote_to_html_node
        )

    def test_block_type_to_helper_function_unordered_list(self):
        """Test block_type_to_helper_function for unordered_list"""
        self.assertEqual(
            block_type_to_helper_function(BlockType.UNORDERED_LIST),
            unordered_list_to_html_node,
        )

    def test_block_type_to_helper_function_ordered_list(self):
        """Test block_type_to_helper_function for ordered_list"""
        self.assertEqual(
            block_type_to_helper_function(BlockType.ORDERED_LIST),
            ordered_list_to_html_node,
        )

    def test_paragraph_to_html_node(self):
        """Test paragraph_to_html_node()"""
        html_node = paragraph_to_html_node("Just some *basic* text")
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, "p")
        self.assertGreaterEqual(len(html_node.children), 1)

    def test_heading_to_html_node(self):
        """Test heading_to_html_node()"""
        html_node = heading_to_html_node("# h1")
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "h1")

    def test_code_to_html_node(self):
        """Test code_to_html_node()"""
        html_node = code_to_html_node("```some code\nblock\nstuff```")
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, "pre")
        self.assertEqual(len(html_node.children), 1)
        self.assertIsInstance(html_node.children[0], LeafNode)
        self.assertEqual(html_node.children[0].tag, "code")

    def test_quote_to_html_node(self):
        """Test quote_to_html_node()"""
        html_node = quote_to_html_node(">line one>line *decorate* two")
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, "blockquote")
        self.assertGreaterEqual(len(html_node.children), 1)

    def test_unordered_list_to_html_node(self):
        """Test unordered_list_to_html_node()"""
        html_node = unordered_list_to_html_node("* line one\n- line two *with dec*")
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, "ul")
        self.assertGreaterEqual(len(html_node.children), 1)
        for child in html_node.children:
            self.assertIsInstance(child, ParentNode)
            self.assertEqual(child.tag, "li")
            self.assertGreaterEqual(len(child.children), 1)

    def test_ordered_list_to_html_node(self):
        """Test ordered_list_to_html_node()"""
        html_node = ordered_list_to_html_node("1. line one\n2. line two *with dec*")
        self.assertIsInstance(html_node, ParentNode)
        self.assertEqual(html_node.tag, "ol")
        self.assertGreaterEqual(len(html_node.children), 1)
        for child in html_node.children:
            self.assertIsInstance(child, ParentNode)
            self.assertEqual(child.tag, "li")
            self.assertGreaterEqual(len(child.children), 1)


if __name__ == "__main__":
    unittest.main()
