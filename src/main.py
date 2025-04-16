import os
from textnode import TextNode, TextType
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from block_mkdown import *
from inline_mkdown import text_to_textnodes
from blocktype import BlockType
import shutil

def move_contents(src, dest):
    if not os.path.exists(src):
        raise FileNotFoundError("Source folder does not exist")
    shutil.rmtree(dest)
    os.mkdir(dest)
    contents = os.listdir(src)
    for item in contents:
        item_path = os.path.join(src, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, dest)
        elif os.path.isdir(item_path):
            dest_path = os.path.join(dest, item)
            if os.path.exists(dest_path):
                shutil.rmtree(dest_path)
            os.mkdir(dest_path)
            move_contents(item_path, dest_path)

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No title found in markdown")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = ""
    template = ""
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)
    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, des_dir_path):
    if not os.path.exists(dir_path_content):
        raise FileNotFoundError(f"Directory {dir_path_content} does not exist")
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path):
            if item.endswith(".md"):
                dest_path = os.path.join(des_dir_path, item[:-3] + ".html")
                generate_page(item_path, template_path, dest_path)
        elif os.path.isdir(item_path):
            dest_path = os.path.join(des_dir_path, item)
            if not os.path.exists(dest_path):
                os.mkdir(dest_path)
            generate_pages_recursive(item_path, template_path, dest_path)

def main():
    move_contents("static", "public")
    generate_pages_recursive("content", "template.html", "public")

main()