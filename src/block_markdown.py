from enum import StrEnum


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
