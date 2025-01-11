"""Main file, currently used for testing"""

from htmlnode import LeafNode, ParentNode
from textnode import (
    TextNode,
    TextType,
    block_to_block_type,
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
    markdown = """# H1

## H2

### H3

#### H4

##### H5

###### H6

####### H7

> blockquote
> blockquote line 2

1. test
2. test

* test
- test

```
some stuff
```

"""
    for b in markdown_to_blocks(markdown):
        print(block_to_block_type(b))

main()
