import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode(tag="div", value="Hello", props={"class": "greeting"})
        with self.assertRaises(NotImplementedError):
            node.to_html()
    
    def test_props_to_html(self):
        node = HTMLNode(tag="a", props={"href": "http://example.com", "target": "_blank"})
        expected = ' href="http://example.com" target="_blank"'
        actual = node.props_to_html()
        self.assertEqual(actual, expected)

    def test_repr(self):
        node = HTMLNode(tag="p", value="Paragraph", children=[], props={"id": "para1"})
        expected = "HTMLNODE(\n\ttag=p,\n\tvalue=Paragraph,\n\tchildren=[],\n\tprops={'id': 'para1'})"
        actual = repr(node)
        self.assertEqual(actual, expected)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Click here", props={"href": "http://example.com"})
        self.assertEqual(node.to_html(), '<a href="http://example.com">Click here</a>')
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_children_and_props(self):
        child_node = LeafNode("b", "Bold text", {"class": "greeting"})
        parent_node = ParentNode("span", [child_node])
        actual = parent_node.to_html()
        expected = '<span><b class="greeting">Bold text</b></span>'
        self.assertEqual(actual, expected)

    def test_to_html_with_link_child(self):
        child_node = LeafNode("a", "Click here", props={"href": "http://example.com"})
        parent_node = ParentNode("b", [child_node])
        expected = '<b><a href="http://example.com">Click here</a></b>'
        actual = parent_node.to_html()
        self.assertEqual(actual, expected)
    
    def test_to_html_with_many_children(self):
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        parent_node = ParentNode("p", children=children)
        actual = parent_node.to_html()
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(actual, expected)
    
    def test_to_html_with_many_children_and_props(self):
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        parent_node = ParentNode("p", children=children, props={"id": "para1"})
        actual = parent_node.to_html()
        expected = '<p id="para1"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(actual, expected)
    

if __name__ == "__main__":
    unittest.main()
