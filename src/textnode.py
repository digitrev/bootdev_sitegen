"""Basic text node"""

from enum import Enum
import re

from htmlnode import HTMLNode, LeafNode, ParentNode


class TextType(Enum):
    """Text type enumeration: normal, bold, etc..."""

    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class BlockType(Enum):
    """Block type enumeration: paragraph, heading, etc..."""

    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


class TextNode:
    """Text node, defined by text, a type, and an optional url"""

    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            isinstance(other, TextNode)
            and self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def to_html_node(self):
        """Convert self to HTML Leaf Node"""
        tag = None
        value = self.text
        props = None
        match self.text_type:
            case TextType.NORMAL:
                tag = None
            case TextType.BOLD:
                tag = "b"
            case TextType.ITALIC:
                tag = "i"
            case TextType.CODE:
                tag = "code"
            case TextType.LINK:
                tag = "a"
                props = {"href": self.url}
            case TextType.IMAGE:
                tag = "img"
                value = ""
                props = {"src": self.url, "alt": self.text}
            case _:
                raise ValueError("Invalid text node")
        return LeafNode(tag, value, props)


def swap_types(to_change: TextType, type_one: TextType, type_two: TextType):
    """Swap to_change from type_one to type_two or vice-versa"""
    if to_change not in (type_one, type_two):
        raise ValueError("to_change should be one of type_one or type_two")
    return type_one if to_change == type_two else type_two


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
):
    """Split nodes based on delimiter. Anything within the delimiter gets the text_type"""
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
        else:
            if node.text.count(delimiter) % 2 == 1:
                raise ValueError("Missing delimiter")
            new_type = TextType.NORMAL
            for text in node.text.split(delimiter):
                new_nodes.append(TextNode(text, new_type, node.url))
                new_type = swap_types(new_type, TextType.NORMAL, text_type)
    return [n for n in new_nodes if n.text != ""]


def extract_markdown_images(text: str):
    """Extract url and alt text or markdown images"""
    return re.findall(r"!\[([^\]]+)\]\(([^\)]+)\)", text)


def extract_markdown_links(text: str):
    """Extract url and alt text or markdown images"""
    return re.findall(r"\[([^\]]+)\]\(([^\)]+)\)", text)


def split_nodes_image(old_nodes: list[TextNode]):
    """Separate out image nodes"""
    return split_nodes_general(
        old_nodes, TextType.IMAGE, "![{}]({})", extract_markdown_images
    )


def split_nodes_link(old_nodes: list[TextNode]):
    """Separate out link nodes"""
    return split_nodes_general(
        old_nodes, TextType.LINK, "[{}]({})", extract_markdown_links
    )


def split_nodes_general(
    old_nodes: list[TextNode],
    text_type: TextType,
    format_string: str,
    extract_function,
):
    """Split out nodes based on format string and extract function"""
    new_nodes = []
    for n in old_nodes:
        node_text = n.text
        for l in extract_function(n.text):
            split = node_text.split(format_string.format(l[0], l[1]))
            new_nodes.append(TextNode(split[0], n.text_type))
            new_nodes.append(TextNode(l[0], text_type, l[1]))
            node_text = split[1]
        new_nodes.append(TextNode(node_text, n.text_type, n.url))
    return [n for n in new_nodes if n.text != ""]


def text_to_textnodes(text: str):
    """Convert text to list of TextNodes"""
    new_nodes = split_nodes_image([TextNode(text, TextType.NORMAL)])
    new_nodes = split_nodes_link(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
    return new_nodes


def markdown_to_blocks(markdown: str):
    """Convert some markdown to blocks of text"""
    return [line.strip() for line in markdown.split("\n\n") if line.strip() != ""]


def block_to_block_type(block: str):
    """Convert block to BlockType"""
    # headings start with 1-6 '#'
    for n in range(6):
        if block.startswith(f"{'#'*(n+1)} "):
            return BlockType.HEADING

    # code blocks start and end with '```'
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # quote blocks start every line with >
    is_quote_block = True
    for line in block.splitlines():
        if not line.startswith(">"):
            is_quote_block = False
    if is_quote_block:
        return BlockType.QUOTE

    # unordered list blocks start every line with '* ' or '- '
    is_unordered_list = True
    for line in block.splitlines():
        if not line.startswith("* ") and not line.startswith("- "):
            is_unordered_list = False
    if is_unordered_list:
        return BlockType.UNORDERED_LIST

    # ordered list blocks start every line with 'n. ', n >= 1
    is_ordered_list = True
    line_number = 0
    for line in block.splitlines():
        line_number += 1
        if not line.startswith(f"{line_number}. "):
            is_ordered_list = False
    if is_ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str):
    """Convert markdown to full html node"""
    children = []
    for block in markdown_to_blocks(markdown):
        children.append(
            block_type_to_helper_function(block_to_block_type(block))(block)
        )

    return ParentNode("div", children)


def block_type_to_helper_function(block_type: BlockType):
    """Convert block to to appropriate _to_html_node function"""
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node
        case BlockType.HEADING:
            return heading_to_html_node
        case BlockType.CODE:
            return code_to_html_node
        case BlockType.QUOTE:
            return quote_to_html_node
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node


def paragraph_to_html_node(paragraph: str):
    """Convert paragraph string to HTMLNode"""
    return ParentNode("p", [tn.to_html_node() for tn in text_to_textnodes(paragraph)])


def heading_to_html_node(heading: str):
    """Convert heading string to HTMLNode"""
    heading_level = len(heading) - len(heading.lstrip("#"))
    heading_text = heading.replace(f"{'#'*heading_level} ", "")
    return ParentNode(f"h{heading_level}", [tn.to_html_node() for tn in text_to_textnodes(heading_text)])


def code_to_html_node(code: str):
    """Convert code string to HTMLNode"""
    code_text = code.strip("```").strip()
    return ParentNode("pre", [LeafNode("code", code_text)])


def quote_to_html_node(quote: str):
    """Convert quote string to HTMLNode"""
    quote_text = "\n".join(l.lstrip(">").strip() for l in quote.splitlines())
    return ParentNode("blockquote", [tn.to_html_node() for tn in text_to_textnodes(quote_text)])


def unordered_list_to_html_node(unordered: str):
    """Convert unordered list string to HTMLNode"""
    children = []
    for line in unordered.splitlines():
        line_text = line.lstrip("*-").lstrip()
        children.append(ParentNode("li", [tn.to_html_node() for tn in text_to_textnodes(line_text)]))
    return ParentNode("ul", children)


def ordered_list_to_html_node(ordered: str):
    """Convert ordered list string to HTMLNode"""
    children = []
    for line in ordered.splitlines():
        line_text = line.lstrip("1234567890.").lstrip()
        children.append(ParentNode("li", [tn.to_html_node() for tn in text_to_textnodes(line_text)]))
    return ParentNode("ol", children)
