from enum import StrEnum

from src.htmlnode import HTMLNode, ParentNode
from src.inline_markdown import text_to_textnodes
from src.textnode import TextNode, TextType, text_node_to_html_node


class BlockType(StrEnum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(document: str) -> list[str]:
    filtered_blocks = []
    md_blocks = document.split("\n\n")
    for md_block in md_blocks:
        block = md_block.strip()
        if not block:
            continue

        filtered_blocks.append(block)

    return filtered_blocks


def block_to_block_type(text_block: str) -> BlockType:
    # Markdown symbol at beginning, end, or both
    if text_block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if text_block.startswith("```") and text_block.endswith("```"):
        return BlockType.CODE

    # Markdown symbol at each line
    lines = text_block.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.ULIST
    if all(line.startswith(f"{i + 1}. ") for i, line in enumerate(lines)):
        return BlockType.OLIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)

    return ParentNode("div", children=children)


def block_to_html_node(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)

    raise ValueError("Invalid Block Type")


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(tn) for tn in text_nodes]


def paragraph_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    paragraph = " ".join(lines)
    return ParentNode("p", children=text_to_children(paragraph))


def heading_to_html_node(block: str) -> HTMLNode:
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    header = block[level + 1 :]
    return ParentNode(f"h{level}", children=text_to_children(header))


def code_to_html_node(block: str) -> HTMLNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")

    raw_node = TextNode(block[4:-3], TextType.TEXT)
    return ParentNode(
        "pre",
        children=[ParentNode("code", children=[text_node_to_html_node(raw_node)])],
    )


def quote_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")

        new_lines.append(line[2:])

    return ParentNode("blockquote", children=text_to_children(" ".join(new_lines)))


def ulist_to_html_node(block: str) -> HTMLNode:
    items = block.split("\n")
    html_items = [
        ParentNode("li", children=text_to_children(item[2:])) for item in items
    ]
    return ParentNode("ul", children=html_items)


def olist_to_html_node(block: str) -> HTMLNode:
    items = block.split("\n")
    html_items = [
        ParentNode("li", children=text_to_children(item[3:])) for item in items
    ]
    return ParentNode("ol", children=html_items)
