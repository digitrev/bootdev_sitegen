"""Module providing LeafNode"""

from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    """Leaf nodes, cannot contain children, must contain value"""
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("Missing value")

        if self.tag is not None:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return self.value
