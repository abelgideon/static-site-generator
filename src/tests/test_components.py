import unittest

from components.htmlnode import HTMLNode
from components.leafnode import LeafNode
from components.parentnode import ParentNode
from components.textnode import TextNode, TextType


class TestComponents(unittest.TestCase):
    def test_prop_to_html(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )

        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

    def test_prop_to_html_2(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
                "alt": "google website",
            }
        )

        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com" target="_blank" alt="google website"',
        )

    def test_prop_to_html_3(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
            }
        )

        self.assertEqual(
            node.props_to_html(),
            ' href="https://www.google.com"',
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Big Title")
        self.assertEqual(node.to_html(), "<h1>Big Title</h1>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_equal_texttype(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_equal_text(self):
        node = TextNode("This is a text", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_equal_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://www.google.com")
        node2 = TextNode(
            "This is a text node", TextType.LINK, "https://www.youtube.com"
        )
        self.assertNotEqual(node, node2)
