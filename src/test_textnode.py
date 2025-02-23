import unittest

from textnode import TextNode, TextType
from htmlnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_eq2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    def test_eq3(self):
        node = TextNode("This is a text node", TextType.CODE, "https://n-leezy.com")
        node2 = TextNode("This is a text node", TextType.CODE, "https://n-leezy.com")
        self.assertEqual(node, node2)
    def test_eq4(self):
        node = TextNode("This is a text node", TextType.CODE, "https://n-leezy.com")
        node2 = TextNode("This is a text node", TextType.CODE, "https://noahlisk.com")
        self.assertNotEqual(node, node2)

class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_node_to_html_node(self):
        self.assertEqual(text_node_to_html_node(TextNode("Hello, world!", TextType.TEXT)), LeafNode("Hello, world!"))
        
    def test_text_node_bold_text(self):
        self.assertEqual(text_node_to_html_node(TextNode("Hello, world!", TextType.BOLD)), LeafNode("Hello, world!", tag="b"))

    def test_text_node_italic_text(self):
        self.assertEqual(text_node_to_html_node(TextNode("Hello, world!", TextType.ITALIC)), LeafNode("Hello, world!", tag="i"))

    def test_text_node_code_text(self):
        self.assertEqual(text_node_to_html_node(TextNode("Hello, world!", TextType.CODE)), LeafNode("Hello, world!", tag="code"))

    def test_text_node_link_text(self):
        self.assertEqual(text_node_to_html_node(TextNode("Hello, world!", TextType.LINK, "https://www.google.com")), LeafNode("Hello, world!", tag="a", props={"href": "https://www.google.com"}))
        
    def test_text_node_image_text(self):
        self.assertEqual(text_node_to_html_node(TextNode("Hello, world!", TextType.IMAGE, "https://www.google.com")), LeafNode("", tag="img", props={"src": "https://www.google.com", "alt": "Hello, world!"}))




if __name__ == "__main__":
    unittest.main()