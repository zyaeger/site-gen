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


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(tn) for tn in text_nodes]


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            html_node = ParentNode(
                "p", children=text_to_children(block.replace("\n", " "))
            )
        elif block_type == BlockType.HEADING:
            header_num = block.count("#")
            html_node = ParentNode(f"h{header_num}", children=text_to_children(block))
        elif block_type == BlockType.CODE:
            node = TextNode(block.replace("```", ""), TextType.CODE)
            html_node = ParentNode("pre", children=[text_node_to_html_node(node)])
        elif block_type == BlockType.QUOTE:
            html_node = ParentNode(
                "blockquote", children=text_to_children(block.replace(">", ""))
            )
        elif block_type == BlockType.ULIST:
            children = []
            for line in block.split("\n"):
                child_node = ParentNode(
                    "li", children=text_to_children(line.replace("- ", ""))
                )
                children.append(child_node)
            html_node = ParentNode("ul", children=children)
        elif block_type == BlockType.OLIST:
            children = []
            for line in block.split("\n"):
                child_node = ParentNode(
                    "li", children=text_to_children(line.split(". ", 1)[1])
                )
                children.append(child_node)
            html_node = ParentNode("ol", children=children)
        else:
            raise ValueError("Invalid Block Type")

        children.append(html_node)

    parent_node = ParentNode("div", children=children)
    return parent_node
