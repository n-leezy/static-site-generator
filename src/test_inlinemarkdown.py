import unittest

from inline_markdown import *
from textnode import *

class TestInlineMarkdown(unittest.TestCase):
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

    def test_split_nodes_delimiter_all_bold(self):
        node = TextNode("This is all bold", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is all bold", TextType.BOLD)])

    def test_extract_markdown_images(self):
        text = "This is a test image ![alt text](image.png)"
        self.assertEqual(extract_markdown_images(text), [("alt text", "image.png")])

    def test_extract_markdown_links(self):
        text = "This is a test link [alt text](https://www.google.com)"
        self.assertEqual(extract_markdown_links(text), [("alt text", "https://www.google.com")])

    def test_split_nodes_images(self):
        node = TextNode("This is a test image ![alt text](image.png)", TextType.TEXT)
        new_nodes = split_nodes_images([node])
        self.assertEqual(new_nodes, [TextNode("This is a test image ", TextType.TEXT), TextNode("alt text", TextType.IMAGE, "image.png")])

    def test_split_nodes_links(self):
        node = TextNode("This is a test link [alt text](https://www.google.com)", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertEqual(new_nodes, [TextNode("This is a test link ", TextType.TEXT), TextNode("alt text", TextType.LINK, "https://www.google.com")])

    def test_split_nodes_images_no_images(self):
        node = TextNode("This is a test text", TextType.TEXT)
        new_nodes = split_nodes_images([node])
        self.assertEqual(new_nodes, [node])

    def test_split_nodes_links_no_links(self):
        node = TextNode("This is a test text", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertEqual(new_nodes, [node])

    def test_split_nodes_images_multiple_images(self):
        node = TextNode("This is a test image ![alt text](image.png) and another image ![alt text](image2.png)", TextType.TEXT)
        new_nodes = split_nodes_images([node])
        self.assertEqual(new_nodes, [TextNode("This is a test image ", TextType.TEXT), TextNode("alt text", TextType.IMAGE, "image.png"), TextNode(" and another image ", TextType.TEXT), TextNode("alt text", TextType.IMAGE, "image2.png")])

    def test_split_nodes_links_multiple_links(self):
        node = TextNode("This is a test link [alt text](https://www.google.com) and another link [alt text](https://www.yahoo.com)", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertEqual(new_nodes, [TextNode("This is a test link ", TextType.TEXT), TextNode("alt text", TextType.LINK, "https://www.google.com"), TextNode(" and another link ", TextType.TEXT), TextNode("alt text", TextType.LINK, "https://www.yahoo.com")])

    def test_split_nodes_images_multiple_images_trailing_text(self):
        node = TextNode("This is a test image ![alt text](image.png) and another image ![alt text](image2.png) and some text", TextType.TEXT)
        new_nodes = split_nodes_images([node])
        self.assertEqual(new_nodes, [TextNode("This is a test image ", TextType.TEXT), TextNode("alt text", TextType.IMAGE, "image.png"), TextNode(" and another image ", TextType.TEXT), TextNode("alt text", TextType.IMAGE, "image2.png"), TextNode(" and some text", TextType.TEXT)])

    def test_split_nodes_links_multiple_links_trailing_text(self):
        node = TextNode("This is a test link [alt text](https://www.google.com) and another link [alt text](https://www.yahoo.com) and some text", TextType.TEXT)
        new_nodes = split_nodes_links([node])
        self.assertEqual(new_nodes, [TextNode("This is a test link ", TextType.TEXT), TextNode("alt text", TextType.LINK, "https://www.google.com"), TextNode(" and another link ", TextType.TEXT), TextNode("alt text", TextType.LINK, "https://www.yahoo.com"), TextNode(" and some text", TextType.TEXT)])

    def test_text_to_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_nodes(text)
        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )

    def test_text_to_nodes_two_bold_words(self):
        text = "This is **bold** and **bold2**"
        nodes = text_to_nodes(text)
        self.assertEqual(nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold2", TextType.BOLD),
        ])

    def test_text_to_nodes_other_test(self):
        text = "This is a _test_ with a `code block` and an ![image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_nodes(text)
        self.assertEqual(nodes, [
            TextNode("This is a ", TextType.TEXT),
            TextNode("test", TextType.ITALIC),
            TextNode(" with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])
    
    
if __name__ == "__main__":
    unittest.main()