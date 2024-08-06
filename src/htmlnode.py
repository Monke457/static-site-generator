class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""
        html = ""
        for key, val in self.props.items():
            html += f" {key}=\"{val}\""

        return html

    def __eq__(self, obj):
        return (self.tag == obj.tag and
                self.value == obj.value and
                self.children == obj.children and
                self.props == obj.props)

    def __repr__(self):
        return ("HTMLNode("
                f"{self.tag},"
                f"{self.value},"
                f"{self.children},"
                f"{self.props})")


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Node must have a value")
        if self.tag is None:
            return self.value
        return (f"<{self.tag}"
                f"{super().props_to_html()}>"
                f"{self.value}</{self.tag}>")


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Node must have a tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("Node must have children")

        html = f"<{self.tag}{super().props_to_html()}>"
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"
        return html
