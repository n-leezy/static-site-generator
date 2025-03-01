import os
import shutil

from block_markdown import markdown_to_blocks, block_to_block_type
from inline_markdown import split_nodes_images
from textnode import *


# Function that recursively copies all contents from static directory to public directory
def copy_static(src, dst, first_call=True):
    # Only delete the destination on the first call
    if first_call and os.path.exists(dst):
        shutil.rmtree(dst)
    
    # Create the destination directory if it doesn't exist
    if not os.path.exists(dst):
        os.mkdir(dst)
    
    # Now for each item in the source directory...
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        
        if os.path.isfile(s):
            # If it's a file, copy it
            shutil.copy(s, d)
            print(f"Copied {s} to {d}")
        else:
            # If it's a directory, recursively copy it
            # Pass False to indicate this is not the first call
            copy_static(s, d, False)  

# Function that extracts the title from a given markdown file
def extract_title(markdown_file: str):
    with open(markdown_file, "r") as f:
        lines = f.readlines()
    
    # Find the first header (h1) and return its text
    for line in lines:
        if line.startswith("# "):
            return line.split(" ", 1)[1].strip()
    raise Exception("No title found in markdown file: " + markdown_file)
