import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="a", value="link",
                        props={"href": "https://www.google.com"})
        node2 = HTMLNode(tag="a", value="link",
                         props={"href": "https://www.google.com"})
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode("a", "This is a html node",
                        props={"href": "https://www.google.com",
                               "target": "_blank"})
        props_html = node.props_to_html()
        self.assertEqual(props_html,
                         " href=\"https://www.google.com\" target=\"_blank\"")


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode(tag="a", value="link",
                        props={"href": "https://www.google.com"})
        node2 = LeafNode(tag="a", value="link",
                         props={"href": "https://www.google.com"})
        self.assertEqual(node, node2)

    def test_to_html(self):
        node = LeafNode("a", "link",
                        props={"href": "https://www.google.com",
                               "target": "_blank"})
        node_html = node.to_html()
        self.assertEqual(
                node_html,
                ("<a href=\"https://www.google.com\" "
                 "target=\"_blank\">link</a>"))


class TestParentNode(unittest.TestCase):
    def test_parentnode_no_children(self):
        node = ParentNode(tag="p", children=[])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_1_child(self):
        child = LeafNode(tag="a", value="link",
                         props={"href": "https://www.google.com"})
        parent = ParentNode(tag="p", children=[child])

        html = parent.to_html()

        self.assertEqual(html, (
            "<p>"
            "<a href=\"https://www.google.com\">link</a>"
            "</p>"
        ))

    def test_to_html_with_children(self):
        child = LeafNode(tag="span", value="spanny")
        child2 = LeafNode(tag="span", value="spanny2")
        child3 = LeafNode(tag="div", value="divvy")

        parent = ParentNode(tag="p", children=[child, child2, child3])

        html = parent.to_html()

        self.assertEqual(html, (
            "<p>"
            "<span>spanny</span>"
            "<span>spanny2</span>"
            "<div>divvy</div>"
            "</p>"
        ))

    def test_to_html_nested(self):
        child = LeafNode(tag="span", value="spanny")
        child2 = LeafNode(tag="span", value="spanny2")
        child3 = LeafNode(tag="div", value="divvy")

        parent = ParentNode(tag="div", children=[child, child2])
        parent2 = ParentNode(tag="div", children=[parent, child3])
        parent3 = ParentNode(tag="div", children=[parent2])

        html = parent3.to_html()

        self.assertEqual(html, (
            "<div><div>"
            "<div>"
            "<span>spanny</span>"
            "<span>spanny2</span>"
            "</div>"
            "<div>divvy</div>"
            "</div></div>"
        ))


if __name__ == "__main__":
    unittest.main()
