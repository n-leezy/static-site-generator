import re

from htmlnode import *
from textnode import *
from inline_markdown import *
from blocknode import *


# Function that takes a raw markdown string as input and returns a list of "block" strings
def markdown_to_blocks(text: str):
    # First, strip leading and trailing whitespace from the entire text
    text = text.strip()
    
    # Use a more robust regex to split blocks by one or more blank lines
    # This will match any sequence of whitespace that includes at least two newlines
    blocks = re.split(r'\n\s*\n', text)
    
    # Create a new list to store non-empty blocks with whitespace trimmed
    result = []
    for block in blocks:
        # Only add non-empty blocks after stripping whitespace
        stripped_block = block.strip()
        if stripped_block:
            result.append(stripped_block)
    return result


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
                level = 0
                for char in block:
                    if char == "#":
                        level += 1
                    else:
                        break
                if level + 1 >= len(block):
                    raise ValueError(f"invalid heading level: {level}")
                text = block[level + 1 :]
                children.append(ParentNode(f"h{level}", text_to_children(text)))
            case BlockType.PARAGRAPH:
                # Replace the newlines with a space and normalize whitespace
                block = block.replace("\n", " ")
                # Normalize whitespace by replacing multiple spaces with a single space
                block = re.sub(r"\s+", " ", block).strip()
                children.append(ParentNode("p", text_to_children(block)))
            case BlockType.QUOTE:
                lines = block.split("\n")
                list_children = []
                for item in lines:
                    if not item.startswith(">"):
                        raise ValueError("invalid quote block")
                list_children = [item.lstrip(">").strip() for item in lines]
                list_children = [item for item in list_children if item]  # Remove empty strings
                content = " ".join(list_children)
                children.append(ParentNode("blockquote", text_to_children(content)))
            case BlockType.UNORDERED_LIST:
                # Get the unordered list items
                list_items = block.split("\n")
                list_children = []
                # Iterate through the list items and create a list of HTML nodes
                for list_item in list_items:
                    # Find the inline markdown of the list item
                    text = list_item[2:]
                    list_children.append(ParentNode("li", text_to_children(text)))
                # Surround the list items with a ul tag
                children.append(ParentNode("ul", list_children))
            case BlockType.ORDERED_LIST:
                # Get the ordered list items
                list_items = block.split("\n")
                list_children = []
                # Iterate through the list items and create a list of HTML nodes
                for list_item in list_items:
                    # Find the inline markdown of the list item
                    text = list_item[3:]
                    list_children.append(ParentNode("li", text_to_children(text)))
                # Surround the list items with a ol tag
                children.append(ParentNode("ol", list_children))
            case BlockType.CODE:
                # Get the code block
                code_block = block.split("```")[1]
                # Strip leading whitespace from each line
                lines = code_block.strip().split("\n")
                # Remove common leading whitespace from all lines
                stripped_lines = []
                for line in lines:
                    stripped_lines.append(line.strip())
                # Join the lines with newlines and add a trailing newline
                code_block = "\n".join(stripped_lines) + "\n"
                # Manually create the TextNode for the code block
                code_node = TextNode(code_block, TextType.CODE)
                # Convert the TextNode to an HTML node and wrap it in a list
                html_node = text_node_to_html_node(code_node)
                children.append(ParentNode("pre", [html_node]))
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
