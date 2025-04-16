import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, World!")
        self.assertEqual(node.to_html(), '<p>Hello, World!</p>')

    def test_leaf_to_html_div(self):
        node = LeafNode("div", "Hello, World!")
        self.assertEqual(node.to_html(), '<div>Hello, World!</div>')
    
    def test_leaf_to_html_prop(self):
        node = LeafNode("p", "Hello, World!", {"class": "text"})
        self.assertEqual(node.to_html(), '<p class="text">Hello, World!</p>')

    def test_leaf_to_html_props(self):
        node = LeafNode("p", "Hello, World!", {"class": "text", "id": "main"})
        self.assertEqual(node.to_html(), '<p class="text" id="main">Hello, World!</p>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, World!")
        self.assertEqual(node.to_html(), "Hello, World!")

if __name__ == "__main__":
    unittest.main()