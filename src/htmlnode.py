from textnode import TextType,TextNode
import textnode


class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        raise NotImplementedError("not impelemented")


    def props_to_html(self):
        if isinstance(self.props,dict):
            new_str = ""
            for key,value in self.props.items():
                new_str += ' ' + key + '=' + '"' + value + '"'
            return new_str
        return "" 


    def __repr__(self):
        return f"HTMLNode=(tag={self.tag},value={self.value},children={self.children},props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self,tag=None,value=None,props=None):
        if value == None:
            raise ValueError("LeafNode must have value")
        super().__init__(tag=tag,value=value,children=None,props=props)


    def to_html(self):
        if self.tag == None:
            return self.value
        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self,tag,children,props=None):
        super().__init__(tag=tag,children=children,props=props,value=None)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode must have tag")
        if self.children == None:
            raise ValueError("LeafNode must have value")

        new_string = ""
        for i in self.children:
            new_string += i.to_html()
        return f"<{self.tag}>{new_string}</{self.tag}>"



def text_node_to_html_node(text_node:TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b",value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i",value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code",value=text_node.text)
        case TextType.LINK:
            return LeafNode(tag="a",props={"href":text_node.url},value=text_node.text)
        case TextType.IMAGE:
            return LeafNode(tag="img",value="",props={"src":text_node.url,"alt":text_node.text})
        case _:
            raise Exception("undefined type")
        


