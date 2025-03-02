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

# Function that generates a webpage given a source path, template path, and destination path
def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    source = ""
    template = ""
    # Read the source and template files
    with open(from_path, "r") as f:
        source = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    
    # Get the HTML content
    content = markdown_to_html_node(source)
    # Get the header
    title = extract_title(from_path)

    # Replace the {{Title}} and {{Content}} placeholders in template.html
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{Content}}", content.to_html())

    # Check if the dest_path exists
    if os.path.exists(dest_path):
        # Write the HTML to the destination file
        with open(dest_path, "w") as f:
            f.write(template)
    else:
        # Create the directory
        os.makedirs(dest_path)
        # Write the HTML to the destination file
        with open(dest_path, "w") as f:
            f.write(template)
    