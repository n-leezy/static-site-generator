from __future__ import annotations # Needed for type hinting in Python 3.10
from textnode import TextNode, TextType

# This is a base class for all HTML nodes.
class HTMLNode:
    def __init__(self, tag: str=None, value: str=None, children: list[HTMLNode]=None, props: dict[str, str]=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props is None:
            return ""
        return " " + " ".join([f"{k}={v}" for k, v in self.props.items()])
    
    def __repr__(self):
        return f"HTMLNode(tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props})"
    
# This is a leaf node, which is a node that has a value and no children.
class LeafNode(HTMLNode):
    def __init__(self, value: str, tag: str=None, props: dict[str, str]=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Value is required for leaf nodes")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __eq__(self, other):
        return self.value == other.value and self.tag == other.tag and self.props == other.props
    
    def __repr__(self):
        return f"LeafNode(value: {self.value}, tag: {self.tag}, props: {self.props})"

# This is a parent node, which is a node that has children and a tag
class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str]=None):
        super().__init__(tag, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag is required for parent nodes")
        if self.children is None:
            raise ValueError("Children are required for parent nodes")
        return f"<{self.tag}{self.props_to_html()}>{''.join([child.to_html() for child in self.children])}</{self.tag}>"
    
    def __eq__(self, other):
        return self.tag == other.tag and self.children == other.children and self.props == other.props
    
    def __repr__(self):
        return f"ParentNode(tag: {self.tag}, children: {self.children}, props: {self.props})"
    
def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(text_node.text)
        case TextType.BOLD:
            return LeafNode(text_node.text, tag="b")
        case TextType.ITALIC:
            return LeafNode(text_node.text, tag="i")
        case TextType.CODE:
            return LeafNode(text_node.text, tag="code")
        case TextType.LINK:
            return LeafNode(text_node.text, tag="a", props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("", tag="img", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid text node type: {text_node.text_type}")
