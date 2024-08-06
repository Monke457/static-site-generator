from htmlnode import LeafNode
from enum import Enum
import utils


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, obj):
        return (self.text == obj.text and
                self.text_type == obj.text_type and
                self.url == obj.url)

    def __repr__(self):
        return f"TextNode({self.text},{self.text_type},{self.url})"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(value=text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", props={
                "src": text_node.url,
                "alt": text_node.text})
        case _:
            raise Exception("Invalid type")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception(f"You may be missing a closing '{delimiter}'")

        for i in range(len(parts)):
            if i % 2 == 0:
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
                continue
            new_nodes.append(TextNode(parts[i], text_type))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        images = utils.extract_markdown_images(node.text)

        if len(images) == 0:
            new_nodes.append(node)
            continue
        text = node.text

        for image in images:
            pattern = f"![{image[0]}]({image[1]})"
            idx = text.index(pattern)
            new_nodes.append(TextNode(text[:idx], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            text = text[idx+len(pattern):]

        if len(text) > 0:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        links = utils.extract_markdown_links(node.text)

        if len(links) == 0:
            new_nodes.append(node)
            continue

        text = node.text
        for link in links:
            pattern = f"[{link[0]}]({link[1]})"
            idx = text.index(pattern)
            new_nodes.append(TextNode(text[:idx], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            text = text[idx+len(pattern):]

        if len(text) > 0:
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    return nodes
