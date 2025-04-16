from blocktype import BlockType
from textnode import text_node_to_html_node, TextNode, TextType
from parentnode import ParentNode
from inline_mkdown import text_to_textnodes

def markdown_to_blocks(markdown):
    blocks = []
    for line in markdown.split("\n\n"):
        if line.strip() == "":
            continue
        blocks.append(line.strip())
    return blocks

def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        for line in block.split("\n"):
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif block.startswith("- "):
        for line in block.split("\n"):
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif block[0] == "1" and block[1] == ".":
        num = 1
        for line in block.split("\n"):
            if not line.startswith(f"{num}. "):
                return BlockType.PARAGRAPH
            num += 1
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
def text_to_children(nodes, tag):
    return ParentNode(tag, [text_node_to_html_node(node) for node in nodes])

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                node = text_to_children(text_to_textnodes(" ".join(block.split("\n"))), "p")
                html_nodes.append(node)
            case BlockType.HEADING:
                level = 0
                for char in block:
                    if char == "#":
                        level += 1
                    else:
                        break
                if level + 1 >= len(block):
                    raise ValueError("Invalid heading")
                block = block[level + 1:]
                node = text_to_children(text_to_textnodes(block), f"h{level}")
                html_nodes.append(node)
            case BlockType.CODE:
                block = block.strip("`").lstrip()
                node = text_node_to_html_node(TextNode(block, TextType.CODE))
                html_nodes.append(ParentNode("pre", [node]))
            case BlockType.QUOTE:
                block = " ".join([line.lstrip(">").strip() for line in block.split("\n")])
                node = text_to_children(text_to_textnodes(block), "blockquote")
                html_nodes.append(node)
            case BlockType.UNORDERED_LIST:
                items = block.split("\n")
                children = [text_to_children(text_to_textnodes(item[2:]), "li") for item in items]
                node = ParentNode("ul", children)
                html_nodes.append(node)
            case BlockType.ORDERED_LIST:
                items = block.split("\n")
                children = [text_to_children(text_to_textnodes(item[3:]), "li") for item in items]
                node = ParentNode("ol", children)
                html_nodes.append(node)
            case _:
                raise ValueError(f"Unknown block type: {block}")
    return ParentNode("div", html_nodes)