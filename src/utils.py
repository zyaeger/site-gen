import re

from src.textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        split_nodes = []
        split_node_text = node.text.split(delimiter)
        if len(split_node_text) % 2 == 0:
            raise Exception(
                "Invalid Markdown syntax. Corresponding closing delimeter not detected."
            )
        for idx, text in enumerate(split_node_text):
            if text == "":
                continue
            if idx % 2 == 0:
                split_nodes.append(TextNode(text, TextType.TEXT))
            else:
                split_nodes.append(TextNode(text, text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple]:
    img_regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(img_regex, text)


def extract_markdown_links(text: str) -> list[tuple]:
    link_regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(link_regex, text)


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        node_text = node.text
        links = extract_markdown_links(node_text)
        if not links or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        for link_text, link in links:
            split_node_text = node_text.split(f"[{link_text}]({link})", 1)
            if len(split_node_text) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            
            if split_node_text[0]:
                new_nodes.append(TextNode(split_node_text[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link))
            node_text = split_node_text[1]

        if node_text:
            new_nodes.append(TextNode(node_text, TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        node_text = node.text
        images = extract_markdown_images(node_text)
        if not images or node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        for image_alt, image_link in images:
            split_node_text = node_text.split(f"![{image_alt}]({image_link})", 1)
            if len(split_node_text) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            
            if split_node_text[0]:
                new_nodes.append(TextNode(split_node_text[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            node_text = split_node_text[1]

        if node_text:
            new_nodes.append(TextNode(node_text, TextType.TEXT))

    return new_nodes
