import re
import textnode as tn

from htmlnode import ParentNode, LeafNode


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def markdown_to_blocks(markdown):
    blocks = []
    for block in markdown.split('\n\n'):
        block = block.strip(" ")
        if len(block) == 0:
            continue
        blocks.append(block)
    return blocks


def block_to_block_type(block):
    if re.match(r"#{1,6} (.*?)", block):
        return "heading"

    if len(block) > 5 and block[:3] == "```" and block[-3:] == "```":
        return "code"

    if len(list(
            filter(
                lambda line: len(line) < 2 or line[:2] != "> ",
                block.split('\n'))
            )) == 0:
        return "quote"

    if len(list(
            filter(
                lambda line: len(line) < 2 or line[:2] != "* ",
                block.split('\n'))
            )) == 0:
        return "unordered_list"

    if len(list(
            filter(
                lambda line: len(line) < 2 or line[:2] != "- ",
                block.split('\n'))
            )) == 0:
        return "unordered_list"

    lines = block.split('\n')
    for i in range(len(lines)):
        num = i+1
        if lines[i][0] != str(num):
            return "paragraph"
        if not re.match(r"\d\. (.*?)", lines[i]):
            return "paragraph"

    return "ordered_list"


def text_to_child_nodes(text):
    res = []
    nodes = tn.text_to_textnodes(text)
    for node in nodes:
        res.append(tn.text_node_to_html_node(node))
    return res


def markdown_to_html_node(markdown):
    root_node = ParentNode("div", [])
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        match block_to_block_type(block):
            case "paragraph":
                parent_node = ParentNode("p", text_to_child_nodes(block))
                root_node.children.append(parent_node)

            case "heading":
                level = len(block.split(' ')[0])
                parent_node = ParentNode(
                        f"h{level}", text_to_child_nodes(block[level+1:]))
                root_node.children.append(parent_node)

            case "code":
                parent_node = ParentNode(
                        "code", text_to_child_nodes(block[3:-3]))
                root_node.children.append(parent_node)

            case "quote":
                lines = filter(lambda line: len(line) > 0, block.split('\n'))
                lines = map(lambda line: line[2:], lines)
                parent_node = ParentNode(
                        "blockquote", text_to_child_nodes("\n".join(lines)))
                root_node.children.append(parent_node)

            case "unordered_list":
                lines = filter(lambda line: len(line) > 0, block.split('\n'))
                parent_node = ParentNode(
                        "ul",
                        list(map(lambda line: ParentNode(
                            "li", text_to_child_nodes(line[2:])), lines)
                        ))
                root_node.children.append(parent_node)

            case "ordered_list":
                lines = filter(lambda line: len(line) > 0, block.split('\n'))
                parent_node = ParentNode(
                        "ol",
                        list(map(lambda line: ParentNode(
                            "li", text_to_child_nodes(line[3:])), lines)
                        ))
                root_node.children.append(parent_node)
    return root_node


def extract_title(markdown):
    head = re.findall(r"^# (.*?)$", markdown, re.M)
    if len(head) == 0:
        raise Exception("markdown must have a title (top level header).\
                Example title:")
    return head[0].strip(" ")


def generate_page(from_path, template_path, dest_path):
    print((f"generating page from {from_path} "
           f"to {dest_path} using {template_path}"))

    content = open(from_path).read()
    html = markdown_to_html_node(content).to_html()
    title = extract_title(content)

    template = open(template_path).read()
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    open(dest_path, "x").write(template)
