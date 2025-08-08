class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
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
