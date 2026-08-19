from textnode import TextNode, TextType


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
