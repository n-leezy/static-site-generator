import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)
    def test_eq2(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)
    def test_eq3(self):
        node = TextNode("This is a text node", TextType.CODE_TEXT, "https://n-leezy.com")
        node2 = TextNode("This is a text node", TextType.CODE_TEXT, "https://n-leezy.com")
        self.assertEqual(node, node2)
    def test_eq4(self):
        node = TextNode("This is a text node", TextType.CODE_TEXT, "https://n-leezy.com")
        node2 = TextNode("This is a text node", TextType.CODE_TEXT, "https://noahlisk.com")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()