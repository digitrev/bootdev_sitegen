"""Main file, currently used for testing"""

from htmlnode import LeafNode, ParentNode


def main():
    """Main function"""
    child = LeafNode("b", "bold")
    child2 = LeafNode("i", "hi bye")
    parent = ParentNode("p", [child, child2])
    print(parent.to_html())

main()
