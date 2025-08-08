import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_neq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_neq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_neq_url(self):
        node = TextNode("This is a link", TextType.LINK, "http://example.com")
        node2 = TextNode("This is a link", TextType.LINK, "http://different.com")
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a link", TextType.LINK, "http://example.com")
        self.assertEqual(node.url, "http://example.com")
    
    def test_no_url(self):
        node = TextNode("This is plain text", TextType.TEXT)
        self.assertIsNone(node.url)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_link(self):
        node = TextNode("Click here", TextType.LINK, "http://foo.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props["href"], node.url)
    
    def test_image(self):
        node = TextNode("alt_text", TextType.IMAGE, "http://cdn.bar.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], node.url)
        self.assertEqual(html_node.props["alt"], node.text)


if __name__ == "__main__":
    unittest.main()
