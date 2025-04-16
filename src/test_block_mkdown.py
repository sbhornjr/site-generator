import unittest
from block_mkdown import markdown_to_blocks, block_to_block_type, markdown_to_html_node
from blocktype import BlockType

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_extra_space(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line        

- This is a list
- with items

    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_blocktype_heading1(self):
        md = "# Heading 1"
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.HEADING)

    def test_block_to_blocktype_heading2(self):
        md = "## Heading 2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.HEADING)

    def test_block_to_blocktype_heading3(self):
        md = "### Heading 3"
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.HEADING)

    def test_block_to_blocktype_heading4(self):
        md = "# Heading 4"
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.HEADING)

    def test_block_to_blocktype_heading5(self):
        md = "# Heading 5"
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.HEADING)

    def test_block_to_blocktype_heading6(self):
        md = "# Heading 6"
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.HEADING)

    def test_block_to_blocktype_heading_no_space(self):
        md = "##Heading 1"
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.PARAGRAPH)

    def test_block_to_blocktype_code(self):
        md = "```python\nprint('Hello, World!')\n```"
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.CODE)

    def test_block_to_blocktype_code_not_3(self):
        md = "``python\nprint('Hello, World!')\n``"
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.PARAGRAPH)

    def test_block_to_blocktype_code_no_ending(self):
        md = "```python\nprint('Hello, World!')\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.PARAGRAPH)

    def test_block_to_blocktype_quote(self):
        md = "> This is a quote"
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.QUOTE)

    def test_block_to_blocktype_quote_multiple(self):
        md = "> This is a quote\n> This is another quote"
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.QUOTE)

    def test_block_to_blocktype_quote_not_all_quotes(self):
        md = "> This is a quote\nThis is not a quote\n> This is another quote"
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.PARAGRAPH)

    def test_block_to_blocktype_unordered_list(self):
        md = "- This is an unordered list\n- with items"
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.UNORDERED_LIST)

    def test_block_to_blocktype_unordered_list_no_space(self):
        md = "-This is an unordered list\n-with items"
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.PARAGRAPH)

    def test_block_to_blocktype_unordered_list_not_all_list(self):
        md = "- This is an unordered list\nwith items\n- and more items"
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.PARAGRAPH)

    def test_block_to_blocktype_ordered_list(self):
        md = "1. This is an ordered list\n2. with items"
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.ORDERED_LIST)

    def test_block_to_blocktype_ordered_list_no_space(self):
        md = "1.This is an ordered list\n2.with items"
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.PARAGRAPH)

    def test_block_to_blocktype_ordered_list_not_all_list(self):
        md = "1. This is an ordered list\nwith items\n2. and more items"
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.PARAGRAPH)

    def test_block_to_blocktype_ordered_list_wrong_order(self):
        md = "1. This is an ordered list\n3. with items"
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.PARAGRAPH)

    def test_block_to_blocktype_paragraph(self):
        md = "This is a paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = """
# This is a heading

This is regular text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1><p>This is regular text</p></div>",
        )

    def test_quotes(self):
        md = """
# This is a heading

>This is
> a quote
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1><blockquote>This is a quote</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
# This is a heading

- This is a list
- with items
- and more items
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1><ul><li>This is a list</li><li>with items</li><li>and more items</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
# This is a heading

1. This is a list
2. with items
3. and more items
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1><ol><li>This is a list</li><li>with items</li><li>and more items</li></ol></div>",
        )

if __name__ == "__main__":
    unittest.main()