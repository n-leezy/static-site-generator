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
    # If there are no matches, return None
    if len(matches) == 0:
        return None
    for alt_text, url in matches:
        image_links.append((alt_text, url))
    return image_links

# Function that takes raw markdown text and returns a list of tuples - tuples contain the alt text and the link url
def extract_markdown_links(text: str):
    markdown_links = []
    markdown_link_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(markdown_link_pattern, text)
    # If there are no matches, return None
    if len(matches) == 0:
        return None
    for alt_text, url in matches:
        markdown_links.append((alt_text, url))
    return markdown_links


# TODO: Fix when there are multiple images
# Function that takes a list of TextNodes and returns a new list of TextNodes with the images split into separate TextNodes
def split_nodes_images(old_nodes: list[TextNode]):
    new_nodes = []
    # Iterate through the old nodes
    for node in old_nodes:
        # If the node is not a text node, add it to the new nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            # Extract the images from the text
            extracted_images = extract_markdown_images(node.text)
            # If there are no images, add the node to the new nodes
            if extracted_images is None:
                new_nodes.append(node)
                continue
            for alt_text, url in extracted_images:
                # Split the text into sections based on the specified image and alt text
                text_to_split = node.text
                sections = text_to_split.split(f"![{alt_text}]({url})", 1)  
                # Add the text before the image to the new nodes
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                # Add the image to the new nodes
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                # Add the text after the image to the new nodes
                if sections[1] != "":
                    new_nodes.append(TextNode(sections[1], TextType.TEXT))
    return new_nodes

                    

# TODO: Fix when there are multiple links
# Function that takes a list of TextNodes and returns a new list of TextNodes with the links split into separate TextNodes
def split_nodes_links(old_nodes: list[TextNode]):
    new_nodes = []
    # Iterate through the old nodes
    for node in old_nodes:
        # If the node is not a text node, add it to the new nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            # Extract the links from the text
            extracted_links = extract_markdown_links(node.text)
            # If there are no links, add the node to the new nodes
            if extracted_links is None:
                new_nodes.append(node)
                continue
            for alt_text, url in extracted_links:
                text_to_split = node.text
                sections = text_to_split.split(f"[{alt_text}]({url})", 1)
                # Add the text before the link to the new nodes
                if sections[0] != "":
                    new_nodes.append(TextNode(sections[0], TextType.TEXT))
                # Add the link to the new nodes
                new_nodes.append(TextNode(alt_text, TextType.LINK, url))
                # Add the text after the link to the new nodes
                if sections[1] != "":
                    new_nodes.append(TextNode(sections[1], TextType.TEXT))
    return new_nodes