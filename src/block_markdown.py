from enum import Enum

from components.htmlnode import HTMLNode
from components.parentnode import ParentNode
from components.textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown: str):
    blocks = markdown.split("\n\n")
    filtered: list[str] = []

    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered.append(block)

    return filtered


def block_to_block_type(block: str) -> BlockType:
    lines = block.splitlines()

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    elif block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown=markdown)
    sub_nodes: list[HTMLNode] = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            if block.startswith("# "):
                value = block.removeprefix("# ")
                sub_nodes.append(ParentNode(tag="h1", children=text_to_children(value)))
            elif block.startswith("## "):
                value = block.removeprefix("## ")
                sub_nodes.append(ParentNode(tag="h2", children=text_to_children(value)))
            elif block.startswith("### "):
                value = block.removeprefix("### ")
                sub_nodes.append(ParentNode(tag="h3", children=text_to_children(value)))
            elif block.startswith("#### "):
                value = block.removeprefix("#### ")
                sub_nodes.append(ParentNode(tag="h4", children=text_to_children(value)))
            elif block.startswith("##### "):
                value = block.removeprefix("##### ")
                sub_nodes.append(ParentNode(tag="h5", children=text_to_children(value)))
            else:
                value = block.removeprefix("###### ")
                sub_nodes.append(ParentNode(tag="h6", children=text_to_children(value)))
        elif block_type == BlockType.PARAGRAPH:
            block = block.replace("\n", " ")
            sub_nodes.append(ParentNode(tag="p", children=text_to_children(block)))
        elif block_type == BlockType.QUOTE:
            lines = block.splitlines()
            values: list[str] = []

            for line in lines:
                values.append(line.removeprefix(">").strip())

            sub_nodes.append(
                ParentNode(
                    tag="blockquote", children=text_to_children(" ".join(values))
                )
            )
        elif block_type == BlockType.ULIST:
            lines = block.splitlines()
            ul_children: list[HTMLNode] = []

            for line in lines:
                line = line.removeprefix("- ")
                ul_children.append(
                    ParentNode(tag="li", children=text_to_children(line))
                )

            ul_parent = ParentNode(tag="ul", children=ul_children)
            sub_nodes.append(ul_parent)
        elif block_type == BlockType.OLIST:
            lines = block.splitlines()
            ol_children: list[HTMLNode] = []
            i = 1

            for line in lines:
                line = line.removeprefix(f"{i}. ")
                ol_children.append(
                    ParentNode(tag="li", children=text_to_children(line))
                )
                i += 1

            ol_parent = ParentNode(tag="ol", children=ol_children)
            sub_nodes.append(ol_parent)
        elif block_type == BlockType.CODE:
            value = block.removeprefix("```")
            value = value.removesuffix("```")
            value = value.removeprefix("\n")

            code_node = TextNode(text=value, text_type=TextType.CODE)
            code_node_html = text_node_to_html_node(code_node)
            pre_node = ParentNode(tag="pre", children=[code_node_html])

            sub_nodes.append(pre_node)

    parent_of_all = ParentNode(tag="div", children=sub_nodes)
    return parent_of_all


def text_to_children(text: str):
    children: list[HTMLNode] = []
    nodes = text_to_textnodes(text)
    for node in nodes:
        children.append(text_node_to_html_node(text_node=node))

    return children
