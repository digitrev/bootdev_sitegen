from textnode import TextNode, TextType
from htmlnode import HTMLNode
from leafnode import LeafNode

def main():
    n1 = LeafNode("p", "This is a paragraph of text.")
    n2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    print(n1.to_html())
    print(n2.to_html())

main()