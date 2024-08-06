import unittest
import textnode

from textnode import TextNode, TextType
from htmlnode import LeafNode



class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_to_html_node(self):
        text_node = TextNode("This is a text node", TextType.TEXT)
        text_html = textnode.text_node_to_html_node(text_node)
        self.assertIsInstance(text_html, LeafNode)

        bold_node = TextNode("This is a bold node", TextType.BOLD)
        bold_html = textnode.text_node_to_html_node(bold_node)
        self.assertIsInstance(bold_html, LeafNode)

        italic_node = TextNode("This is an italic node", TextType.ITALIC)
        italic_html = textnode.text_node_to_html_node(italic_node)
        self.assertIsInstance(italic_html, LeafNode)

        code_node = TextNode("This is a code node", TextType.CODE)
        code_html = textnode.text_node_to_html_node(code_node)
        self.assertIsInstance(code_html, LeafNode)

        link_node = TextNode("A link", TextType.LINK, "https://www.boot.dev")
        link_html = textnode.text_node_to_html_node(link_node)
        self.assertIsInstance(link_html, LeafNode)

        image_node = TextNode("alt", TextType.IMAGE, "https://www.boot.dev")
        image_html = textnode.text_node_to_html_node(image_node)
        self.assertIsInstance(image_html, LeafNode)

    def test_split_nodes_delimiter_code(self):
        text_node = TextNode("This is a text node", TextType.TEXT)
        new_nodes = textnode.split_nodes_delimiter([text_node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[0].text, "This is a text node")

        text_node = TextNode("A `code containing` text node", TextType.TEXT)
        new_nodes = textnode.split_nodes_delimiter([text_node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[0].text, "A ")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[1].text, "code containing")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, " text node")

        text_node = TextNode("A `code` text `containing` node", TextType.TEXT)
        new_nodes = textnode.split_nodes_delimiter([text_node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[0].text, "A ")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, " text ")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)
        self.assertEqual(new_nodes[3].text, "containing")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[4].text, " node")

        text_node = TextNode("A `code containing` text node", TextType.TEXT)
        text_node2 = TextNode("A text node `with code`", TextType.TEXT)
        new_nodes = textnode.split_nodes_delimiter(
                [text_node, text_node2], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 6)
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[0].text, "A ")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[1].text, "code containing")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, " text node")
        self.assertEqual(new_nodes[3].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "A text node ")
        self.assertEqual(new_nodes[4].text_type, TextType.CODE)
        self.assertEqual(new_nodes[4].text, "with code")
        self.assertEqual(new_nodes[5].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[5].text, "")

    def test_split_nodes_delimiter_bold(self):
        text_node = TextNode("A **bolded** text node", TextType.TEXT)
        new_nodes = textnode.split_nodes_delimiter([text_node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[0].text, "A ")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[1].text, "bolded")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, " text node")

    def test_split_nodes_delimiter_italic(self):
        text_node = TextNode("A _italic_ text node", TextType.TEXT)
        new_nodes = textnode.split_nodes_delimiter([text_node], "_", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[0].text, "A ")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[1].text, "italic")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[2].text, " text node")

    def test_split_nodes_delimiter_error(self):
        text_node = TextNode("A _italic text node", TextType.TEXT)
        with self.assertRaises(Exception):
            textnode.split_nodes_delimiter([text_node], "_", TextType.ITALIC)

    def test_split_node_image(self):
        node = TextNode(("This is text with an "
                         "image ![of something](/path/to/something.jpg) and "
                         "![of something else](/path/to/something-else.jpg)"),
                        TextType.TEXT)
        new_nodes = textnode.split_nodes_image([node])
        self.assertEqual(new_nodes,
                         [
                             TextNode("This is text with an image ", TextType.TEXT),
                             TextNode("of something", TextType.IMAGE, "/path/to/something.jpg"),
                             TextNode(" and ", TextType.TEXT),
                             TextNode("of something else", TextType.IMAGE, "/path/to/something-else.jpg")
                             ])

    def test_split_node_link(self):
        node = TextNode(("This is text with a link "
                         "[to something](www.something.com) and "
                         "[to something else](www.somethingelse.com)"),
                        TextType.TEXT)
        new_nodes = textnode.split_nodes_link([node])
        self.assertEqual(new_nodes,
                         [
                             TextNode("This is text with a link ", TextType.TEXT),
                             TextNode("to something", TextType.LINK, "www.something.com"),
                             TextNode(" and ", TextType.TEXT),
                             TextNode("to something else", TextType.LINK, "www.somethingelse.com")
                             ])

    def test_text_to_textnodes(self):
        text = ("This is **text** with an *italic* word "
                "and a `code block` and an "
                "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
                "and a [link](https://boot.dev)")
        nodes = textnode.text_to_textnodes(text)
        self.assertEqual(nodes,
                         [
                             TextNode("This is ", TextType.TEXT),
                             TextNode("text", TextType.BOLD),
                             TextNode(" with an ", TextType.TEXT),
                             TextNode("italic", TextType.ITALIC),
                             TextNode(" word and a ", TextType.TEXT),
                             TextNode("code block", TextType.CODE),
                             TextNode(" and an ", TextType.TEXT),
                             TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                             TextNode(" and a ", TextType.TEXT),
                             TextNode("link", TextType.LINK, "https://boot.dev")
                             ])


if __name__ == "__main__":
    unittest.TextNode()
