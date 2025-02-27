from inline_markdown import split_nodes_images
from textnode import *

def main():
    text_node = TextNode("noah", TextType.ITALIC, "https://noahlisk.com")
    node = TextNode("This is a test image ![alt text](image.png", TextType.TEXT)
    new_nodes = split_nodes_images([node])
    print(new_nodes)

if __name__ == "__main__":
    main()
