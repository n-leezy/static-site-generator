import re

from htmlnode import *
from textnode import *


# Splits a list of TextNodes based on a delimiter and returns a new list of TextNodes
def split_nodes_delimiter(old_nodes: list[TextNode], delimeter: str, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        # If the node is not a text node, add it to the new nodes
        if node.text_type != TextType.TEXT: 
            new_nodes.append(node) 
        else:  
            # If the node is a text node, split it into new text nodes based on the delimeter
            split_nodes = []
            sections = node.text.split(delimeter)
            if len(sections) % 2 == 0:
                raise ValueError("invalid Markdown, formatted section not closed")
            for i in range(len(sections)):
                # Skip empty sections
                if sections[i] == "":
                    continue
                # Add text nodes for even sections
                if i % 2 == 0:
                    split_nodes.append(TextNode(sections[i], text_type.TEXT))
                # Add nodes specified by the delimeter for odd sections
                else:
                    split_nodes.append(TextNode(sections[i], text_type))
            new_nodes.extend(split_nodes)
    return new_nodes

# Function that takes raw markdown text and returns a list of tuples - tuples contain the alt text and the image url
def extract_markdown_images(text: str):
    image_links = []
    image_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    # Find all matches in the text and extract the alt text and url
    matches = re.findall(image_pattern, text)
    for alt_text, url in matches:
        image_links.append((alt_text, url))
    return image_links

# Function that takes raw markdown text and returns a list of tuples - tuples contain the alt text and the link url
def extract_markdown_links(text: str):
    markdown_links = []
    markdown_link_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(markdown_link_pattern, text)
    for alt_text, url in matches:
        markdown_links.append((alt_text, url))
    return markdown_links
