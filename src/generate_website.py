import os
import shutil
import pathlib

from block_markdown import *
from inline_markdown import *
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
    template = template.replace("{{ Content }}", content.to_html())

    # Check if the dest_path exists and is a directory - if so, remove it
    if os.path.isdir(dest_path):
        os.rmdir(dest_path)  # Remove the directory if it exists
    
    # Make sure the parent directory exists
    parent_dir = os.path.dirname(dest_path)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir)
        
    # Write the HTML to the destination file
    with open(dest_path, "w") as f:
        f.write(template)


# Function that recursively generates the pages from the content directory
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Get a list of all files in the content directory
    files = os.listdir(dir_path_content)
    # Generate a new .html file for every markdown file found using the template.html
    for file in files:
        if file.endswith(".md"):
            generate_page(os.path.join(dir_path_content, file), template_path, os.path.join(dest_dir_path, file).replace(".md", ".html"))

    # Get a list of all directories in the content directory
    directories = [d for d in os.listdir(dir_path_content) if os.path.isdir(os.path.join(dir_path_content, d))]
    # Generate a new directory for every directory found
    for directory in directories:
        generate_pages_recursive(os.path.join(dir_path_content, directory), template_path, os.path.join(dest_dir_path, directory))