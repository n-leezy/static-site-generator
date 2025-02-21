from __future__ import annotations

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
        return " ".join([f"{k}={v}" for k, v in self.props.items()])
    
    def __repr__(self):
        return f"HTMLNode(tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict[str, str]=None):
        super().__init__(tag, value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Value is required for leaf nodes")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode(tag: {self.tag}, value: {self.value}, props: {self.props})"
        