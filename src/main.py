import os
import shutil
import sys

from block_markdown import markdown_to_blocks, block_to_block_type
from inline_markdown import split_nodes_images
from textnode import *
from generate_website import *

def main():
    
    copy_static("static", "docs")
    # Use sys.argv to grab the first CLI argument
    basepath = "/" if len(sys.argv) < 2 else sys.argv[1]
    generate_pages_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()