import re

from htmlnode import *
from textnode import *
from inline_markdown import *
from blocknode import *


# Function that takes a raw markdown string as input and returns a list of "block" strings
def markdown_to_blocks(text: str):
    blocks = []
    # Split the text into blocks
    blocks = re.split(r"\n\n", text)
    # Iterate through the blocks and remove empty blocks and trim whitespace
    for block in blocks:
        if block == "":
            blocks.remove(block)
        else:
            blocks[blocks.index(block)] = block.strip(" ")
    return blocks


# Function that takes a single block of markdown text as input and returns the BlockType
def block_to_block_type(block: str):
    # Check if the block is a heading
    if block.startswith("#"):
        return BlockType.HEADING
    # Check if the block is a code block
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    # Check if the block is a quote
    elif block.startswith(">"):
        quote_blocks = block.split("\n")
        for quote_block in quote_blocks:
            if not quote_block.startswith(">"):
                continue
            else:
                return BlockType.QUOTE
    # Check if the block is an unordered list
    elif block.startswith("-"):
        unordered_list_blocks = block.split("\n")
        for unordered_list_block in unordered_list_blocks:
            if not unordered_list_block.startswith("-"):
                continue
            else:
                return BlockType.UNORDERED_LIST
    # Check if the block is an ordered list
    elif block.startswith("1."):
        ordered_list_blocks = block.split("\n")
        count = 0
        for ordered_list_block in ordered_list_blocks:
            if not ordered_list_block.startswith(f"{count+1}."):
                continue
            else:
                count += 1
        if count > 0:
            return BlockType.ORDERED_LIST
    # If none of the above, the block is a paragraph
    else:
        return BlockType.PARAGRAPH

# Function that takes a full markdown document as input and outputs a single parent HTML node
# The parent HTML node will have child HTML nodes representing the nested elements
def markdown_to_html_node(text: str):
    blocks = markdown_to_blocks(text)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                # Get the heading level
                heading_level = block.count("#", 0, block.index(" "))
                # Get the heading text
                heading_text = block.split("#")[1].strip()
                # Create a heading HTML node
                children.append(ParentNode(f"h{heading_level}", text_to_children(heading_text)))
            case BlockType.PARAGRAPH:
                children.append(ParentNode("p", text_to_children(block)))
            case BlockType.QUOTE:
                children.append(ParentNode("blockquote", text_to_children(block)))
            case BlockType.UNORDERED_LIST:
                # Get the unordered list items
                list_items = block.split("\n")
                list_children = []
                # Iterate through the list items and create a list of HTML nodes
                for list_item in list_items:
                    # Find the inline markdown of the list item
                    list_children.append(ParentNode("li", text_to_children(list_item)))
                # Surround the list items with a ul tag
                children.append(ParentNode("ul", list_children))
            case BlockType.ORDERED_LIST:
                # Get the ordered list items
                list_items = block.split("\n")
                list_children = []
                # Iterate through the list items and create a list of HTML nodes
                for list_item in list_items:
                    # Find the inline markdown of the list item
                    list_children.append(ParentNode("li", text_to_children(list_item)))
                # Surround the list items with a ol tag
                children.append(ParentNode("ol", list_children))
            case BlockType.CODE:
                # Get the code block
                code_block = block.split("```")[1]
                # Manually create the TextNode for the code block
                code_node = TextNode(code_block, TextType.CODE)
                # Convert the TextNode to an HTML node
                children.append(ParentNode("pre",text_node_to_html_node(code_node)))
            case _:
                raise ValueError(f"Invalid block type: {block_type}")
    return ParentNode("div", children)


# Helper function that takes a string of text and returns a list of HTML nodes
def text_to_children(text: str):
    children_text_nodes = text_to_nodes(text)
    inline_html_nodes = []
    for child in children_text_nodes:
        inline_html_nodes.append(text_node_to_html_node(child))
    return inline_html_nodes
