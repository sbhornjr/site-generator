import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        node = HTMLNode("div", "Hello")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_props(self):
        node = HTMLNode("div", "Hello", None, {"class": "container", "id": "main"})
        self.assertEqual(node.props_to_html(), ' class="container" id="main"')

    def test_repr(self):
        node = HTMLNode("div", "Hello", None, {"class": "container"})
        self.assertEqual(repr(node), "HTMLNode(div, Hello, None, {'class': 'container'})")

if __name__ == "__main__":
    unittest.main()