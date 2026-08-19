import unittest

from components.textnode import TextNode, TextType
from functions.splitnodedelim import split_nodes_delimiter


class TestSplitNodeDelim(unittest.TestCase):
    def test_bold(self):
        node = TextNode(text="a**b**cd", text_type=TextType.TEXT)
        nodelist = split_nodes_delimiter(
            old_nodes=[node], text_type=TextType.BOLD, delimiter="**"
        )

        self.assertEqual(
            nodelist,
            [
                TextNode(text="a", text_type=TextType.TEXT),
                TextNode(text="b", text_type=TextType.BOLD),
                TextNode(text="cd", text_type=TextType.TEXT),
            ],
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_italic(self):
        node = TextNode(text="a_b_cd", text_type=TextType.TEXT)
        nodelist = split_nodes_delimiter(
            old_nodes=[node], text_type=TextType.ITALIC, delimiter="_"
        )

        self.assertEqual(
            nodelist,
            [
                TextNode(text="a", text_type=TextType.TEXT),
                TextNode(text="b", text_type=TextType.ITALIC),
                TextNode(text="cd", text_type=TextType.TEXT),
            ],
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_code(self):
        node = TextNode(text="a`b`cd", text_type=TextType.TEXT)
        nodelist = split_nodes_delimiter(
            old_nodes=[node], text_type=TextType.CODE, delimiter="`"
        )

        self.assertEqual(
            nodelist,
            [
                TextNode(text="a", text_type=TextType.TEXT),
                TextNode(text="b", text_type=TextType.CODE),
                TextNode(text="cd", text_type=TextType.TEXT),
            ],
        )

    def test_special_start(self):
        node = TextNode(text="**a**bcd", text_type=TextType.TEXT)
        nodelist = split_nodes_delimiter(
            old_nodes=[node], text_type=TextType.BOLD, delimiter="**"
        )

        self.assertEqual(
            nodelist,
            [
                TextNode(text="a", text_type=TextType.BOLD),
                TextNode(text="bcd", text_type=TextType.TEXT),
            ],
        )

    def test_special_end(self):
        node = TextNode(text="abc**d**", text_type=TextType.TEXT)
        nodelist = split_nodes_delimiter(
            old_nodes=[node], text_type=TextType.BOLD, delimiter="**"
        )

        self.assertEqual(
            nodelist,
            [
                TextNode(text="abc", text_type=TextType.TEXT),
                TextNode(text="d", text_type=TextType.BOLD),
            ],
        )

    def test_list(self):
        node1 = TextNode(text="**a**bcd", text_type=TextType.TEXT)
        node2 = TextNode(text="a**b**cd", text_type=TextType.TEXT)
        node3 = TextNode(text="ab**c**d", text_type=TextType.TEXT)
        node4 = TextNode(text="abc**d**", text_type=TextType.TEXT)

        nodelist = split_nodes_delimiter(
            old_nodes=[node1, node2, node3, node4],
            text_type=TextType.BOLD,
            delimiter="**",
        )

        self.assertEqual(
            nodelist,
            [
                TextNode(text="a", text_type=TextType.BOLD),
                TextNode(text="bcd", text_type=TextType.TEXT),
                TextNode(text="a", text_type=TextType.TEXT),
                TextNode(text="b", text_type=TextType.BOLD),
                TextNode(text="cd", text_type=TextType.TEXT),
                TextNode(text="ab", text_type=TextType.TEXT),
                TextNode(text="c", text_type=TextType.BOLD),
                TextNode(text="d", text_type=TextType.TEXT),
                TextNode(text="abc", text_type=TextType.TEXT),
                TextNode(text="d", text_type=TextType.BOLD),
            ],
        )
