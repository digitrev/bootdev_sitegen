"""Module providing ParentNode"""

from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    """Leaf nodes, cannot contain value, must contain children"""
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Missing tag")
        if not self.children:
            raise ValueError("Missing children")
        return "".join([f"<{self.tag}{self.props_to_html()}>"]
                       + [c.to_html() for c in self.children]
                       + [f"</{self.tag}>"])
