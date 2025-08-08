from src.textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        split_nodes = []
        delim_count = node.text.count(delimiter)
        if delim_count == 0:
            split_nodes.append(node)
        if delim_count % 2 == 1:
            raise Exception("Invalid Markdown syntax. Corresponding closing delimeter not detected.")
        split_node_text = node.text.split(delimiter)
        for idx, text in enumerate(split_node_text):
            if text == "":
                continue
            if idx % 2 == 0:
                split_nodes.append(TextNode(text, node.text_type))
            else:
                split_nodes.append(TextNode(text, text_type))

        new_nodes.extend(split_nodes)
    return new_nodes
