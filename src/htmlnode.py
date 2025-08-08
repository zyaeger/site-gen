class HTMLNode:
    def __init__(
        self,
        tag: str = None,
        value: str = None,
        children: list = None,
        props: dict = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children or []
        self.props = props or {}

    def __repr__(self):
        return f"HTMLNODE(\n\ttag={self.tag},\n\tvalue={self.value},\n\tchildren={self.children},\n\tprops={self.props})"

    def to_html(self) -> str:
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self) -> str:
        attr_str = ""
        for key, value in self.props.items():
            attr_str += f' {key}="{value}"'
        return attr_str


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("LeafNode must have a value to convert to HTML")

        if not self.tag:
            return self.value  # Just return the text if no tag is specified

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[LeafNode], props: dict = None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Tag required")
        if not self.children:
            raise ValueError("Children required")

        html = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"
        return html
