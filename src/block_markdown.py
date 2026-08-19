def markdown_to_blocks(markdown: str):
    blocks = markdown.split("\n\n")
    filtered: list[str] = []

    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered.append(block)

    return filtered
