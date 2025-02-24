from htmlnode import *
from textnode import *


# Splits a list of TextNodes based on a delimiter and returns a new list of TextNodes
# Currently only supports single delimiter given in a text string, i.e. "This is a **bold** word"
# TODO: Support multiple delimiters. i.e. "This is multiple **bold** **words**"
def split_nodes_delimiter(old_nodes: list[TextNode], delimeter: str, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        # If the node is not a text node, add it to the new nodes
        if node.text_type != TextType.TEXT: 
            new_nodes.append(node) 
        else:  
            # If the node is a text node, split it into new text nodes based on the delimeter
            text = node.text
            split_lines = text.split(delimeter)
            if len(split_lines) == 1:
                raise ValueError("No delimiter found")
            if len(split_lines) == 2:
                raise ValueError("Matching closed delimiter not found")
            # add the first TextType.TEXT node to the new nodes
            new_nodes.append(TextNode(split_lines[0], text_type.TEXT))
            # add the node specified by the delimeter to the new nodes
            new_nodes.append(TextNode(split_lines[1], text_type))
            # add the third TextType.TEXT node to the new nodes
            new_nodes.append(TextNode(split_lines[2], text_type.TEXT))
    return new_nodes
