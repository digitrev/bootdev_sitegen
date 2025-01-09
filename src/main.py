"""Main file, currently used for testing"""

from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType, extract_markdown_images, extract_markdown_links, split_nodes_delimiter


def main():
    """Main function"""
    text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
    print(extract_markdown_links(text))
# [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

main()
