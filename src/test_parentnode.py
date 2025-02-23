import unittest
from htmlnode import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        parent = ParentNode("div", [LeafNode("Hello, world!", None)])
        self.assertEqual(parent.to_html(), "<div>Hello, world!</div>")

    def test_to_html_with_props(self):
        parent = ParentNode("div", [LeafNode("Hello, world!")], {"class": "test"})
        self.assertEqual(parent.to_html(), "<div class=test>Hello, world!</div>")

    def test_to_html_with_multiple_children(self):
        parent = ParentNode("div", [LeafNode("Hello, world!"), LeafNode("Goodbye, world!")])
        self.assertEqual(parent.to_html(), "<div>Hello, world!Goodbye, world!</div>")

    def test_to_html_with_none_children(self):
        parent = ParentNode("div", None)
        self.assertRaises(ValueError, parent.to_html)

    def test_to_html_with_none_tag(self):
        parent = ParentNode(None, [LeafNode("Hello, world!")])
        self.assertRaises(ValueError, parent.to_html)

    def test_to_html_with_parent_node_as_child(self):
        parent = ParentNode("div", [ParentNode("span", [LeafNode("Hello, world!")])])
        self.assertEqual(parent.to_html(), "<div><span>Hello, world!</span></div>")



if __name__ == "__main__":
    unittest.main()
