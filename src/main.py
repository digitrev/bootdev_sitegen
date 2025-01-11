"""Main file, currently used for testing"""

from htmlnode import LeafNode, ParentNode
from textnode import (
    TextNode,
    TextType,
    block_to_block_type,
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
    markdown_to_html_node,
    paragraph_to_html_node,
    quote_to_html_node,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    swap_types,
    text_to_textnodes,
)


def main():
    """Main function"""
    markdown = """
# Markdown syntax guide

## Headers

# This is a Heading h1
## This is a Heading h2
###### This is a Heading h6

## Emphasis

*This text will be italic*  

**This text will be bold**  

## Lists

### Unordered

* Item 1
* Item 2
* Item 2a
* Item 2b

### Ordered

1. Item 1
2. Item 2
3. Item 3

## Images

![This is an alt text.](/image/sample.webp "This is a sample image.")

## Links

You may be using [Markdown Live Preview](https://markdownlivepreview.com/).

## Blockquotes

> Markdown is a lightweight markup language with plain-text-formatting syntax, created in 2004 by John Gruber with Aaron Swartz.
>
> Third line

## Blocks of code

```
let message = 'Hello world';
alert(message);
```

## Inline code

This web site is using `markedjs/marked`.

"""
    print(markdown_to_html_node(markdown))


main()
