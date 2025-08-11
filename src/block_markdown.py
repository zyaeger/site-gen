def markdown_to_blocks(document: str) -> list[str]:
    filtered_blocks = []
    md_blocks = document.split("\n\n")
    for md_block in md_blocks:
        block = md_block.strip()
        if not block:
            continue

        filtered_blocks.append(block)

    return filtered_blocks
