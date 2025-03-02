import os
import shutil

from block_markdown import markdown_to_blocks, block_to_block_type
from inline_markdown import split_nodes_images
from textnode import *
from generate_website import *

def main():
    
    header_text = extract_title("src/test.md")
    print(header_text)

if __name__ == "__main__":
    main()