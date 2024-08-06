import unittest
import utils

from htmlnode import ParentNode, LeafNode


class TestUtils(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = ("This is text with a "
                "![rick roll](https://i.imgur.com/aKaOqIh.gif)"
                "and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        images = utils.extract_markdown_images(text)
        self.assertEqual(images,
                         [("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                          ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_markdown_links(self):
        text = ("This is text with a "
                "link [to boot dev](https://www.boot.dev) and"
                "[to youtube](https://www.youtube.com/@bootdotdev)")
        links = utils.extract_markdown_links(text)
        self.assertEqual(
                links,
                [("to boot dev", "https://www.boot.dev"),
                 ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_markdown_to_blocks(self):
        markdown = ("# Heading\n\n"
                    "Paragraph with **bold** and *italic*\n\n"
                    "* list item 1\n* list item 2\n* list item 3")
        blocks = utils.markdown_to_blocks(markdown)

        self.assertEqual(blocks, [
            "# Heading",
            "Paragraph with **bold** and *italic*",
            "* list item 1\n* list item 2\n* list item 3"
            ])

    def test_block_to_block_type_headings(self):
        block = "# heading"
        block_type = utils.block_to_block_type(block)
        self.assertEqual(block_type, "heading")

        block = "###### heading"
        block_type = utils.block_to_block_type(block)
        self.assertEqual(block_type, "heading")

        block = "####### heading"
        block_type = utils.block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

        block = "#heading"
        block_type = utils.block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

    def test_block_to_block_type_code(self):
        block = "```code```"
        block_type = utils.block_to_block_type(block)
        self.assertEqual(block_type, "code")

        block = "````code````"
        block_type = utils.block_to_block_type(block)
        self.assertEqual(block_type, "code")

        block = "``code```"
        block_type = utils.block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

        block = "```code"
        block_type = utils.block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

    def test_block_to_block_type_quote(self):
        block = ("> quote\n"
                 "> quote\n"
                 "> quote")
        block_type = utils.block_to_block_type(block)
        self.assertEqual(block_type, "quote")

        block = ("> \n"
                 "> quote\n"
                 "> quote")
        block_type = utils.block_to_block_type(block)
        self.assertEqual(block_type, "quote")

        block = ("something\n"
                 "> quote\n"
                 "> quote")
        block_type = utils.block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

        block = ("> quote\n"
                 "> quote\n"
                 "quote")
        block_type = utils.block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

        block = (">quote\n"
                 ">quote\n"
                 ">quote\n")
        block_type = utils.block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

    def test_block_to_block_type_ul(self):
        block = ("* list\n"
                 "* list\n"
                 "* list")
        block_type = utils.block_to_block_type(block)
        self.assertEqual(block_type, "unordered_list")

        block = ("- list\n"
                 "- list\n"
                 "- list")
        block_type = utils.block_to_block_type(block)
        self.assertEqual(block_type, "unordered_list")

        block = ("*    list\n"
                 "*   list\n"
                 "* list")
        block_type = utils.block_to_block_type(block)
        self.assertEqual(block_type, "unordered_list")

        block = ("* list\n"
                 "- list\n"
                 "- list")
        block_type = utils.block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

        block = ("*list\n"
                 "* list\n"
                 "* list")
        block_type = utils.block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

        block = ("list\n"
                 "* list\n"
                 "* list")
        block_type = utils.block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

        block = ("* list\n"
                 "* list\n"
                 "* list\n")
        block_type = utils.block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

    def test_block_to_block_type_ol(self):
        block = ("1. list\n"
                 "2. list\n"
                 "3. list")
        block_type = utils.block_to_block_type(block)
        self.assertEqual(block_type, "ordered_list")

        block = ("1.    list\n"
                 "2.   list\n"
                 "3. list")
        block_type = utils.block_to_block_type(block)
        self.assertEqual(block_type, "ordered_list")

        block = ("1. list\n"
                 "2. list\n"
                 "list")
        block_type = utils.block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

        block = ("1. list\n"
                 "3. list\n"
                 "2. list")
        block_type = utils.block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

        block = ("2. list\n"
                 "3. list\n"
                 "4. list")
        block_type = utils.block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

        block = ("0. list\n"
                 "1. list\n"
                 "2. list")
        block_type = utils.block_to_block_type(block)
        self.assertEqual(block_type, "paragraph")

    def test_markdown_to_html_simple(self):
        markdown = ("# Heading\n\n"
                    "Paragraph")
        result = utils.markdown_to_html_node(markdown)

        expected = ParentNode("div", children=[
            ParentNode("h1", [LeafNode(value="Heading")]),
            ParentNode("p", [LeafNode(value="Paragraph")])
            ])

        self.assertEqual(result, expected)

    def test_markdown_to_html_node(self):
        markdown = ("# Heading1\n\n"
                    "## Heading2\n\n"
                    "This is just a paragraph with **bold** and *italics*!\n\n"
                    "### Heading3\n\n"
                    "My List\n\n"
                    "* Item 1\n"
                    "* Item 2\n\n"
                    "### Heading3\n\n"
                    "My ordered list\n\n"
                    "1. Item 1\n"
                    "2. Item 2\n\n"
                    "```Some code examples```\n\n"
                    "> quote\n"
                    "> something\n"
                    "> more quote\n\n"
                    "Final paragraph")

        result = utils.markdown_to_html_node(markdown)

        expected = ParentNode("div", [
            ParentNode("h1", [LeafNode(value="Heading1")]),
            ParentNode("h2", [LeafNode(value="Heading2")]),
            ParentNode("p", [
                LeafNode(value="This is just a paragraph with "),
                LeafNode("b", "bold"),
                LeafNode(value=" and "),
                LeafNode("i", "italics"),
                LeafNode(value="!")]),
            ParentNode("h3", [LeafNode(value="Heading3")]),
            ParentNode("p", [LeafNode(value="My List")]),
            ParentNode("ul", [
                ParentNode("li", [LeafNode(value="Item 1")]),
                ParentNode("li", [LeafNode(value="Item 2")])
                ]),
            ParentNode("h3", [LeafNode(value="Heading3")]),
            ParentNode("p", [LeafNode(value="My ordered list")]),
            ParentNode("ol", [
                ParentNode("li", [LeafNode(value="Item 1")]),
                ParentNode("li", [LeafNode(value="Item 2")])
                ]),
            ParentNode("code", [LeafNode(value="Some code examples")]),
            ParentNode("blockquote",
                       [LeafNode(value="quote\nsomething\nmore quote")]),
            ParentNode("p", [LeafNode(value="Final paragraph")])
            ])

        self.assertEqual(result, expected)

    def test_extract_title(self):
        markdown = "# title"
        result = utils.extract_title(markdown)
        self.assertEqual(result, "title")

        markdown = "#title"
        with self.assertRaises(Exception):
            utils.extract_title(markdown)

        markdown = "## title"
        with self.assertRaises(Exception):
            utils.extract_title(markdown)

        markdown = "this is not a valid # title"
        with self.assertRaises(Exception):
            utils.extract_title(markdown)

        markdown = "#    title    "
        result = utils.extract_title(markdown)
        self.assertEqual(result, "title")

        markdown = "# title with space"
        result = utils.extract_title(markdown)
        self.assertEqual(result, "title with space")
