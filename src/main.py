import os
from textnode import TextNode, TextType
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from block_mkdown import *
from inline_mkdown import text_to_textnodes
from blocktype import BlockType
import shutil
import sys

def move_contents(src, dest):
    if not os.path.exists(src):
        raise FileNotFoundError("Source folder does not exist")
    if not os.path.exists(dest):
        os.mkdir(dest)
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

def generate_page(from_path, template_path, dest_path, basepath):
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
    template = template.replace("href=\"/", f"href=\"{basepath}")
    template = template.replace("src=\"/", f"src=\"{basepath}")
    with open(dest_path, "w") as f:
        f.write(template)

def generate_pages_recursive(dir_path_content, template_path, des_dir_path, basepath):
    if not os.path.exists(dir_path_content):
        raise FileNotFoundError(f"Directory {dir_path_content} does not exist")
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path):
            if item.endswith(".md"):
                dest_path = os.path.join(des_dir_path, item[:-3] + ".html")
                generate_page(item_path, template_path, dest_path, basepath)
        elif os.path.isdir(item_path):
            dest_path = os.path.join(des_dir_path, item)
            if not os.path.exists(dest_path):
                os.mkdir(dest_path)
            generate_pages_recursive(item_path, template_path, dest_path, basepath)

def main():
    basepath = "/"
    if len(sys.argv) == 2:
        basepath = sys.argv[1]
    move_contents("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()