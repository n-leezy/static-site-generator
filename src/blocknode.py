from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

class BlockNode:
    def __init__(self, text: str, block_type: BlockType):
        self.text = text
        self.block_type = block_type

    def __eq__(self, other):
        return self.text == other.text and self.block_type == other.block_type
    
    def __repr__(self):
        return f"BlockNode(text={self.text}, block_type={self.block_type})"
    
    