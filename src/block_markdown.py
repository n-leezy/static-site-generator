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
