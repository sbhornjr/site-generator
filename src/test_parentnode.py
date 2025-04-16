import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_to_html_with_parent_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(parent_node.to_html(), '<div class="container"><span>child</span></div>')

    def test_to_html_with_child_props(self):
        child_node = LeafNode("span", "child", {"class": "text"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), '<div><span class="text">child</span></div>')

    def test_to_html_with_multiple_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("span", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><span>child2</span></div>")

    def test_to_html_with_many_props(self):
        child_node1 = LeafNode("span", "child1", {"class": "text"})
        child_node2 = LeafNode("span", "child2", {"class": "text", "id": "child2"})
        parent_node = ParentNode("div", [child_node1, child_node2], {"class": "container"})
        self.assertEqual(parent_node.to_html(), '<div class="container"><span class="text">child1</span><span class="text" id="child2">child2</span></div>')

if __name__ == "__main__":
    unittest.main() 