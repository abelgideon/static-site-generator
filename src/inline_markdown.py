import re

from components.textnode import TextNode, TextType


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    output: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            output.append(node)
        else:
            div = node.text.split(delimiter)

            if len(div) % 2 == 0:
                raise Exception("Invalid Markdown Syntax")

            i = 1
            for text in div:
                if text == "":
                    i += 1
                    continue
                if i % 2 == 0:
                    output.append(TextNode(text=text, text_type=text_type))
                else:
                    output.append(TextNode(text=text, text_type=TextType.TEXT))

                i += 1

    return output


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

            if sections[0] != "":
                output.append(TextNode(sections[0], TextType.TEXT))

            output.append(TextNode(img_text, TextType.IMAGE, img_url))

            remaining_text = sections[1]

        if remaining_text != "":
            output.append(TextNode(remaining_text, TextType.TEXT))

    return output


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    output: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            output.append(node)
            continue

        links = extract_markdown_links(node.text)
        if not links:
            output.append(node)
            continue

        remaining_text = node.text
        for link_text, link_url in links:
            sections = remaining_text.split(f"[{link_text}]({link_url})", 1)

            if sections[0] != "":
                output.append(TextNode(sections[0], TextType.TEXT))

            output.append(TextNode(link_text, TextType.LINK, link_url))

            remaining_text = sections[1]

        if remaining_text != "":
            output.append(TextNode(remaining_text, TextType.TEXT))

    return output


def text_to_textnodes(text: str) -> list[TextNode]:
    node = TextNode(text=text, text_type=TextType.TEXT)

    bold_split = split_nodes_delimiter(
        old_nodes=[node], text_type=TextType.BOLD, delimiter="**"
    )
    italic_split = split_nodes_delimiter(
        old_nodes=bold_split, text_type=TextType.ITALIC, delimiter="_"
    )
    code_split = split_nodes_delimiter(
        old_nodes=italic_split, text_type=TextType.CODE, delimiter="`"
    )
    link_split = split_nodes_link(old_nodes=code_split)
    img_split = split_nodes_image(old_nodes=link_split)

    return img_split
