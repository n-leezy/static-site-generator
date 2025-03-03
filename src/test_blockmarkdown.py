import unittest

from block_markdown import *

class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_with_code_block(self):
        md = """This is a paragraph

```python
print("Hello, world!")
```

This is another paragraph"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph",
                "```python\nprint(\"Hello, world!\")\n```",
                "This is another paragraph",
            ],
        )
        
    def test_markdown_to_blocks_with_list(self):
        md = """This is a paragraph

- This is a list
- with items"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_with_nested_list(self):
        md = """This is a paragraph

- This is a list
    - with items"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph",
                "- This is a list\n    - with items",
            ],
        )

    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type("This is a paragraph"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("- This is a list\n- with items"), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type("1. This is a list\n2. with items"), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type("```python\nprint(\"Hello, world!\")\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)

    def test_markdown_to_html_node_with_paragraphs(self):
        md = """This is **bolded** paragraph 
        text in a p
        tag here 
        
        This is another paragraph with _italic_ text and `code` here"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_markdown_to_html_node_with_code_block(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_markdown_to_html_node_with_list(self):
        md = """This is a paragraph

- This is a unordered list
- with items

1. This is a ordered list
2. with items
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is a paragraph</p><ul><li>This is a unordered list</li><li>with items</li></ul><ol><li>This is a ordered list</li><li>with items</li></ol></div>",
        )
    
    def test_markdown_to_html_node_with_headers(self):
        md = """# This is a header

## This is a subheader

### This is a sub-subheader
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a header</h1><h2>This is a subheader</h2><h3>This is a sub-subheader</h3></div>",
        )
