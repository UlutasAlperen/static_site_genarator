from enum import Enum,auto


class TextType(Enum):
    TEXT = "text"
    LINK = "link"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    IMAGE = "image"

class BlockType(Enum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()


class TextNode:
    def __init__(self,text,text_type: TextType,url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self,other):
        return isinstance(other,TextNode) and (self.text == other.text) and (self.text_type == other.text_type) and (self.url == other.url)


    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"





