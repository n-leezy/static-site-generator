import os
import shutil

from block_markdown import markdown_to_blocks, block_to_block_type
from inline_markdown import split_nodes_images
from textnode import *
from generate_website import *

def main():
    
    copy_static("static", "public")

    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()