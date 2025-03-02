import os
import shutil

from block_markdown import markdown_to_blocks, block_to_block_type
from inline_markdown import split_nodes_images
from textnode import *
from generate_website import *

def main():
    
    copy_static("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()