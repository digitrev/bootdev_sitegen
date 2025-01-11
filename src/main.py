"""Main file, currently used for testing"""

from htmlnode import LeafNode, ParentNode
from textnode import (
    TextNode,
    TextType,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    swap_types,
    text_to_textnodes,
)


def main():
    """Main function"""
    node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev)"
        + " and [to youtube](https://www.youtube.com/@bootdotdev) with trailing text",
        TextType.NORMAL,
    )
    new_nodes = split_nodes_link(
        [node, TextNode("sentence without URL", TextType.BOLD)]
    )
    # print(new_nodes)

    node.text = (
        "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        + " and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    )
    new_nodes = split_nodes_image(
        [node, TextNode("sentence without image", TextType.BOLD)]
    )
    # print(new_nodes)
    print("\n".join(str(x) for x in text_to_textnodes("This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) with trailing text")))


main()
