from enum import Enum

from src.htmlnode import LeafNode


class TextType(Enum):
    TEXT = "TEXT"
    BOLD = "BOLD"
    ITALIC = "ITALIC"
    CODE = "CODE"
    LINK = "LINK"
    IMAGE = "IMAGE"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):
    text_node_type = text_node.text_type
    if text_node_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

    raise Exception("text node should be one of TextType")
