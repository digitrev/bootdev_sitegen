"""Basic text node"""

from enum import Enum

from htmlnode import LeafNode

class TextType(Enum):
    """Text type enumeration: normal, bold, etc..."""
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    """Text node, defined by text, a type, and an optional url"""
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url)

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
                value = ""
                props = {"src": self.url, "alt": self.text}
            case _:
                raise ValueError("Invalid text node")
        return LeafNode(tag, value, props)
