import unittest

from textnode import TextNode, TextType
from utils import split_nodes_delimiter

class TestInlineMarkdown(unittest.TestCase):
    def test_code_case(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)
    
    def test_bold_case(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)

    def test_italic_case(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, expected)

    def test_multiple_italic_case(self):
        node = TextNode("This is text with multiple _italic_ words. _Foo_ bar", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is text with multiple ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" words. ", TextType.TEXT),
            TextNode("Foo", TextType.ITALIC),
            TextNode(" bar", TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, expected)
    
    def test_multi_word_bold_case(self):
        node = TextNode("This is text with a **very bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("very bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertListEqual(new_nodes, expected)
