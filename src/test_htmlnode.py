import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("div", "Hello, World!", props={"class": "test"})
        self.assertEqual(node.props_to_html(), "class=test")
    
    def test_repr(self):
        node = HTMLNode("div", "Hello, World!", props={"class": "test"})
        self.assertEqual(repr(node), "tag: div, value: Hello, World!, children: None, props: {'class': 'test'}")

    def test_props_to_html_none(self):
        node = HTMLNode("div", "Hello, World!")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty(self):
        node = HTMLNode("div", "Hello, World!", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_multiple(self):
        node = HTMLNode("div", "Hello, World!", props={"class": "test", "id": "test"})
        self.assertEqual(node.props_to_html(), "class=test id=test")

    def test_props_to_html_multiple_with_none(self):
        node = HTMLNode("div", "Hello, World!", props={"class": "test", "id": None})
        self.assertEqual(node.props_to_html(), "class=test")

if __name__ == "__main__":
    unittest.main()
