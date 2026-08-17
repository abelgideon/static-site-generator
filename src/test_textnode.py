import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_not_equal_texttype(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

    def test_not_equal_text(self):
        node = TextNode("This is a text", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

    def test_not_equal_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.google.com")
        node2 = TextNode(
            "This is a text node", TextType.LINK, "https://www.youtube.com"
        )
        self.assertNotEqual(node, node2)
