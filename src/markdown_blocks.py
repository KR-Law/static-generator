from enum import Enum

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType
import re



class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"


def markdown_to_blocks(markdown):
    lines = markdown.split("\n\n")
    blocks = []
    for line in lines:
        if line.strip() != "":
            blocks.append(line.strip())
    return blocks

def block_to_block_type(block):
    lines = block.split("\n")
    first = lines[0].strip()
    last = lines[-1].strip()
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if first.startswith("```") and last == "```":
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            strip_line = line.lstrip()
            if not strip_line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown):
    """
    Convert a markdown string to an HTML node structure.
    
    This function takes a markdown string, splits it into blocks, converts each
    block to its corresponding HTML node representation, and wraps all the
    resulting nodes in a parent div element.
    
    Args:
        markdown (str): The markdown string to convert to HTML nodes.
        
    Returns:
        ParentNode: A ParentNode object with tag "div" containing all the
                converted markdown blocks as child HTML nodes.
    """
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        elif block_type == BlockType.HEADING:
            return heading_to_html_node(block)
        elif block_type == BlockType.CODE:
            return code_to_html_node(block)
        elif block_type == BlockType.QUOTE:
            return quote_to_html_node(block)
        elif block_type == BlockType.ULIST:
            return ulist_to_html_node(block)
        elif block_type == BlockType.OLIST:
            return olist_to_html_node(block)
        else:
            raise ValueError("invalid block")
        
def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children_nodes = text_to_children(paragraph)
    return ParentNode(tag="p", children=children_nodes)

def heading_to_html_node(block):
    left, _, right = block.lstrip().partition(" ")
    level = len(left)
    if level > 6:
        raise ValueError(f"invalid heading level: {level}")
    return ParentNode(tag=f"h{level}", children=text_to_children(right.rstrip()))

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode(tag="code", children=[child])
    return ParentNode(tag="pre", children=[code])

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        strip_line = line.lstrip()
        if not strip_line.startswith(">"):
            raise ValueError("invalid quote block")
        text = strip_line.lstrip(">").strip()
        if text == "":
            continue
        new_lines.append(strip_line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def ulist_to_html_node(block):
    items = []
    for ln in block.splitlines():
        text = ln.lstrip().removeprefix("-").lstrip()
        li_children = text_to_children(text)
        items.append(ParentNode(tag="li", children = li_children))
    return ParentNode(tag="ul", children=items)
    
def olist_to_html_node(block):
    items = []
    for ln in block.splitlines():
        text = re.sub(r"^\s*\d+.\s+", "", ln)
        li_children = text_to_children(text)
        items.append(ParentNode(tag="li", children=li_children))
    return ParentNode(tag="ol", children=items)