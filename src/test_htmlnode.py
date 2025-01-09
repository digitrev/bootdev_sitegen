"""testing HTML Node"""

import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    """Test HTML Node"""
    def test_gen_tag(self):
        node = HTMLNode(tag="t1")
        self.assertEqual(node.tag, "t1")

    def test_gen_value(self):
        node = HTMLNode(value="v1")
        self.assertEqual(node.value, "v1")

    def test_gen_children(self):
        children = [HTMLNode(), HTMLNode()]
        node = HTMLNode(children=children)
        self.assertEqual(len(node.children), 2)

    def test_gen_props(self):
        node = HTMLNode(props={"href": "google.ca", "alt": "hi"})
        self.assertEqual(node.props, {"href": "google.ca", "alt": "hi"})

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

if __name__ == "__main__":
    unittest.main()