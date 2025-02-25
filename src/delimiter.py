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
