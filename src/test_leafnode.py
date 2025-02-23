import unittest

from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("Hello, World!", "div")
        self.assertEqual(node.to_html(), "<div>Hello, World!</div>")

    def test_to_html_none(self):
        node = LeafNode(None, "div")
        self.assertRaises(ValueError, node.to_html)
    
    def test_to_html_none_tag(self):
        node = LeafNode("Hello, World!", None)
        self.assertEqual(node.to_html(), "Hello, World!")

    def test_repr(self):
        node = LeafNode("Hello, World!", "div")
        self.assertEqual(repr(node), "LeafNode(value: Hello, World!, tag: div, props: None)")