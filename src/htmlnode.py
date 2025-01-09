"""Module providing HTMLNode"""
class HTMLNode():
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
