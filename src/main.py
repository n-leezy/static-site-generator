import os
import shutil

from block_markdown import markdown_to_blocks, block_to_block_type
from inline_markdown import split_nodes_images
from textnode import *
from generate_website import *

def main():
    
    copy_static("static", "public")
    # Use sys.argv to grab the first CLI argument
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    generate_pages_recursive("content", "template.html", "public", basepath)

if __name__ == "__main__":
    main()