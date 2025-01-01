from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main():
    n = HTMLNode(props = {"href": "google.ca", "alt": "hi"})
    print(n)
    print(n.props_to_html())
    print(n.props_to_html()[0])

main()