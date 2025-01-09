"""Main file, currently used for testing"""

from parentnode import ParentNode
from leafnode import LeafNode

def main():
    """Main function"""
    child = LeafNode("b", "bold")
    parent = ParentNode("p", [child])
    print(parent.to_html())

main()
