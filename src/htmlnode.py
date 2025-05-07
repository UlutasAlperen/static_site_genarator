from textnode import TextType,TextNode,BlockType
import re

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
        

def split_nodes_delimiter(old_nodes,delimiter,text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text =node.text
        start = 0 
        while start < len(text):
            delimiter_start = text.find(delimiter, start)
            if delimiter_start == -1:
                new_nodes.append(TextNode(text[start:], TextType.TEXT))
                break

            if delimiter_start > start:
                new_nodes.append(TextNode(text[start:delimiter_start], TextType.TEXT))

            delimiter_end = text.find(delimiter, delimiter_start + len(delimiter))
            if delimiter_end == -1:
                raise Exception(f"Missing closing delimiter '{delimiter}' in text: '{text}'")

            formatted_text = text[delimiter_start + len(delimiter): delimiter_end]
            new_nodes.append(TextNode(formatted_text, text_type))

            start = delimiter_end + len(delimiter)

    return new_nodes



def extract_markdown_images(text):
    return re.findall(r'!\[([^\]]+)\]\(([^)]+)\)',text)



def extract_markdown_links(text):
    return re.findall(r'(?<!!)\[([^\]]+)\]\(([^)]+)\)',text)

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_images(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        text = node.text
        for alt, url in matches:
            full_syntax = f"![{alt}]({url})"
            parts = text.split(full_syntax, 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text = parts[1]
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return [n for n in new_nodes if n.text != ""]


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(node)
            continue

        text = node.text
        for label, url in matches:
            full_syntax = f"[{label}]({url})"
            parts = text.split(full_syntax, 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(label, TextType.LINK, url))
            text = parts[1]
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return [n for n in new_nodes if n.text != ""]


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes


def markdown_to_blocks(markdown):
    if not isinstance(markdown, str):
        raise TypeError("Argument must be a string")

    blocks = []

    for block in markdown.split('\n\n'):
        stripped_block = block.strip()
        if stripped_block:
            blocks.append(stripped_block)

    return blocks


def block_to_block_type(markdown_text):
    lines = markdown_text.split("\n")

    if lines[0] == "```" and lines[-1] == "```":
        return BlockType.CODE

    if lines[0].startswith("#"):
        i = 0
        while i < len(lines[0]) and lines[0][i] == "#":
            i += 1
        if 1 <= i <= 6 and i < len(lines[0]) and lines[0][i] == " ":
            return BlockType.HEADING

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    for i, line in enumerate(lines):
        expected_prefix = f"{i + 1}. "
        if not line.startswith(expected_prefix):
            break
    else:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH




