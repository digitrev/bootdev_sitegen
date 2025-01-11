"""Main file, currently used for testing"""

from htmlnode import LeafNode, ParentNode
from textnode import (
    TextNode,
    TextType,
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    swap_types,
    text_to_textnodes,
)


def main():
    """Main function"""
    markdown = """# This is a heading

  This is a paragraph of text. It has some **bold** and *italic* words inside of it.

  
* This is the first list item in a list block  
* This is a list item  
* This is another list item"""
    for b in markdown_to_blocks(markdown):
        print(b)

main()
