import unittest

from inline_markdown import *
from textnode import *

# Testing nodes with a single delimiter, nested delimiters are not accounted for and should raise an error
class TestDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a 'code block' word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "'", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)])

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("bold", TextType.BOLD), TextNode(" word", TextType.TEXT)])

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with a *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("italic", TextType.ITALIC), TextNode(" word", TextType.TEXT)])

    def test_split_nodes_delimiter_nested(self):
        node = TextNode("This is a nested **bold with *italic* text**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is a nested ", TextType.TEXT), TextNode("bold with *italic* text", TextType.BOLD)])

    def test_split_nodes_delimiter_noclosing_delimiter(self):
        node = TextNode("This is a **incomplete bold word", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_extract_markdown_images(self):
        text = "This is a test image ![alt text](image.png)"
        self.assertEqual(extract_markdown_images(text), [("alt text", "image.png")])

    def test_extract_markdown_links(self):
        text = "This is a test link [alt text](https://www.google.com)"
        self.assertEqual(extract_markdown_links(text), [("alt text", "https://www.google.com")])


if __name__ == "__main__":
    unittest.main()