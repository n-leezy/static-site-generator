import re

from htmlnode import *
from textnode import *
from inline_markdown import *


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
