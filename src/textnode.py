"""Basic text node"""

from enum import Enum
import re

from htmlnode import LeafNode


class TextType(Enum):
    """Text type enumeration: normal, bold, etc..."""

    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    """Text node, defined by text, a type, and an optional url"""

    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def text_node_to_html_node(self):
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
                value = None
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
    return split_nodes_general(old_nodes, TextType.IMAGE, "![{}]({})")


def split_nodes_link(old_nodes: list[TextNode]):
    """Separate out link nodes"""
    return split_nodes_general(old_nodes, TextType.LINK, "[{}]({})")


def split_nodes_general(
    old_nodes: list[TextNode], text_type: TextType, format_string: str
):
    """Split out nodes based"""
    new_nodes = []
    for n in old_nodes:
        node_text = n.text
        for l in extract_markdown_links(n.text):
            split = node_text.split(format_string.format(l[0], l[1]))
            new_nodes.append(TextNode(split[0], n.text_type))
            new_nodes.append(TextNode(l[0], text_type, l[1]))
            node_text = split[1]
        new_nodes.append(TextNode(node_text, n.text_type))
    return [n for n in new_nodes if n.text != ""]
