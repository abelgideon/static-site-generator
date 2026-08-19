from components.textnode import TextNode, TextType
from functions.extractmarkdown import extract_markdown_images


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    output: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            output.append(node)
            continue

        links = extract_markdown_images(node.text)
        if not links:
            output.append(node)
            continue

        remaining_text = node.text
        for img_text, img_url in links:
            sections = remaining_text.split(f"![{img_text}]({img_url})", 1)

            # Append preceding text if not empty
            if sections[0] != "":
                output.append(TextNode(sections[0], TextType.TEXT))

            # Append the link node
            output.append(TextNode(img_text, TextType.IMAGE, img_url))

            remaining_text = sections[1]

        # Append any remaining trailing text
        if remaining_text != "":
            output.append(TextNode(remaining_text, TextType.TEXT))

    return output
