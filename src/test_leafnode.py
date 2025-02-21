import unittest

from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("div", "Hello, World!")
        self.assertEqual(node.to_html(), "<div>Hello, World!</div>")

    def test_to_html_none(self):
        node = LeafNode("div", None)
        self.assertRaises(ValueError, node.to_html)
    
    def test_to_html_none_tag(self):
        node = LeafNode(None, "Hello, World!")
        self.assertEqual(node.to_html(), "Hello, World!")

    def test_repr(self):
        node = LeafNode("div", "Hello, World!")
        self.assertEqual(repr(node), "LeafNode(tag: div, value: Hello, World!, props: None)")