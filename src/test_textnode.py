import unittest
from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is text", TextType.BOLD)
        node2 = TextNode("This is text", TextType.BOLD)
        self.assertEqual(node1, node2)

    def test_not_eq(self):
        node1 = TextNode("This is text", TextType.BOLD)
        node2 = TextNode("This is text", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_eq_with_url(self):
        node1 = TextNode("This is text", TextType.LINK, "http://example.com")
        node2 = TextNode("This is text", TextType.LINK, "http://example.com")
        self.assertEqual(node1, node2)

    def test_not_eq_with_url(self):
        node1 = TextNode("This is text", TextType.LINK, "http://example.com")
        node2 = TextNode("This is text", TextType.LINK, "http://example.org")
        self.assertNotEqual(node1, node2)

    def test_not_eq_different_text(self):
        node1 = TextNode("This is text", TextType.BOLD)
        node2 = TextNode("This is different text", TextType.BOLD)
        self.assertNotEqual(node1, node2)

    def test_not_eq_missing_url(self):
        node1 = TextNode("This is text", TextType.LINK, "http://example.com")
        node2 = TextNode("This is text", TextType.LINK)
        self.assertNotEqual(node1, node2)
        
    def test_repr(self):
        node = TextNode("This is text", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(This is text, TextType.BOLD, None)")
    
    def test_repr_with_url(self):
        node = TextNode("This is text", TextType.LINK, "http://example.com")
        self.assertEqual(repr(node), "TextNode(This is text, TextType.LINK, http://example.com)")

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text")

    def test_italic(self):
        node = TextNode("This is an italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text")

    def test_code(self):
        node = TextNode("This is a code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text")
    
    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "http://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "http://example.com"})
    
    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "http://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "http://example.com/image.png", "alt": "This is an image"})

    def test_unknown_type(self):
        node = TextNode("This is an unknown type", "unknown")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()