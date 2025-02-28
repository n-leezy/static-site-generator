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

if __name__ == "__main__":
    unittest.main()