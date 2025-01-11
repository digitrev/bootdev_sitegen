"""Module providing HTMLNode"""


class HTMLNode:
    """HTML Node - base class"""

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """Returns HTML; not implemented on base class"""
        raise NotImplementedError()

    def props_to_html(self):
        """converts props dictionary to appropriate html"""
        if self.props is not None:
            return "".join([f' {k}="{v}"' for k, v in self.props.items()])
        return ""

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, value):
        return (
            self.tag == value.tag
            and self.value == value.value
            and self.children == value.children
            and self.props == value.props
        )


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


class ParentNode(HTMLNode):
    """Leaf nodes, cannot contain value, must contain children"""

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Missing tag")
        if not self.children:
            raise ValueError("Missing children")
        return "".join(
            [f"<{self.tag}{self.props_to_html()}>"]
            + [c.to_html() for c in self.children]
            + [f"</{self.tag}>"]
        )
