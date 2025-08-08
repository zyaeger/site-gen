import unittest

from htmlnode import HTMLNode


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
        