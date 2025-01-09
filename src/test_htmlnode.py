"""testing HTML Node"""

import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    """Test HTML Node"""
    def test_html_values(self):
        """Test setting tag, value"""
        node = HTMLNode("t1", "value")
        self.assertEqual(node.tag, "t1")
        self.assertEqual(node.value, "value")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_props_to_html(self):
        """Test props_to_html()"""
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_leaf_no_tag(self):
        """Test leaf node, no tag"""
        node = LeafNode(None, "test")
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, "test")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
        self.assertEqual(node.to_html(), "test")

    def test_leaf_with_tag(self):
        """Test leaf node, with tag"""
        node = LeafNode("p", "paragraph")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "paragraph")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
        self.assertEqual(node.to_html(), "<p>paragraph</p>")

    def test_leaf_with_tag_and_props(self):
        """Test leaf node, with tag and props"""
        node = LeafNode("a", "link text", {"href": "google.ca"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "link text")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"href": "google.ca"})
        self.assertEqual(node.to_html(), '<a href="google.ca">link text</a>')

    def test_leaf_with_no_value(self):
        """Test leaf node without value, ensure error raised"""
        node = LeafNode(None, None)
        with self.assertRaises(ValueError) as ve:
            node.to_html()
        self.assertEqual(str(ve.exception), "Missing value")

    def test_parent_with_tag(self):
        """Test parent node with tag, one child"""
        child = LeafNode("b", "test")
        parent = ParentNode("p", [child])
        self.assertEqual(parent.tag, "p")
        self.assertEqual(parent.children, [child])
        self.assertEqual(parent.props, None)
        self.assertEqual(parent.to_html(), 
                         "<p><b>test</b></p>")

    def test_parent_with_tag_and_props(self):
        """Test parent node with tag and props, one child"""
        child = LeafNode("b", "test")
        parent = ParentNode("a", [child], {"href": "google.ca"})
        self.assertEqual(parent.tag, "a")
        self.assertEqual(parent.children, [child])
        self.assertEqual(parent.props, {"href": "google.ca"})
        self.assertEqual(parent.to_html(),
                         '<a href="google.ca"><b>test</b></a>')
    
    def test_parent_no_tag(self):
        """Test parent node without a tag"""
        child = LeafNode("b", "test")
        parent = ParentNode(None, child)
        with self.assertRaises(ValueError) as ve:
            parent.to_html()
        self.assertEqual(str(ve.exception), "Missing tag")

    def test_parent_no_children(self):
        """Test parent node without any children"""
        parent = ParentNode("p", None)
        with self.assertRaises(ValueError) as ve:
            parent.to_html()
        self.assertEqual(str(ve.exception), "Missing children")


if __name__ == "__main__":
    unittest.main()
