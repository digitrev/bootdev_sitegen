"""Main file, currently used for testing"""

from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType, split_nodes_delimiter


def main():
    """Main function"""
    node = TextNode("Simple *bold* text with followup *bold*", TextType.NORMAL)
    node2 = TextNode("Testing *bold* text", TextType.NORMAL)
    new_nodes = split_nodes_delimiter([node, node2], "*", TextType.BOLD)
    print(new_nodes)

main()
