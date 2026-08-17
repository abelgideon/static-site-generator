import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
