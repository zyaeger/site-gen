import unittest

from textnode import TextNode, TextType
from utils import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
)

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


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_single_markdown_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(matches, expected)

    def test_extract_multiple_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertListEqual(matches, expected)
    
    def test_extract_single_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://foo.com)"
        )
        expected = [("link", "https://foo.com")]
        self.assertListEqual(matches, expected)

    def test_extract_multiple_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(matches, expected)
