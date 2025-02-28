from block_markdown import markdown_to_blocks, block_to_block_type
from inline_markdown import split_nodes_images
from textnode import *

def main():
    test_string = """
    This is the first paragraph
    
    This is the second paragraph"""
    blocks = markdown_to_blocks(test_string)
    for block in blocks:
        print(block)
        print(block_to_block_type(block))

if __name__ == "__main__":
    main()
