import unittest

from components.textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_extract_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_delim_bold(self):
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

    def test_delim_italic(self):
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

    def test_delim_code(self):
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

    def test_delim_list(self):
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

    def test_split_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_text_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image_to_html(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.boot.dev", "alt": "This is an image"},
        )

    def test_bold_to_html(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")
