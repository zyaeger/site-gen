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
            raise Exception("Invalid Markdown syntax. Corresponding closing delimeter not detected.")
        for idx, text in enumerate(split_node_text):
            if text == "":
                continue
            if idx % 2 == 0:
                split_nodes.append(TextNode(text, TextType.TEXT))
            else:
                split_nodes.append(TextNode(text, text_type))
        new_nodes.extend(split_nodes)
    return new_nodes
