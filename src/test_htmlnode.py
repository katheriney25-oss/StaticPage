import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType

class TestHTMLNode(unittest.TestCase):

	def test_props_to_html_none(self):
		node = HTMLNode(tag="p")
		self.assertEqual(node.props_to_html(), "")

	def test_props_to_html_empty_dict(self):
		node = HTMLNode(tag="p", props={})
		self.assertEqual(node.props_to_html(), "")

	def test_props_to_html_single_prop(self):
		node = HTMLNode(
			tag="a", 
			props={"href": "https://boot.dev"}
		)
		self.assertEqual(
			node.props_to_html(), 
			' href="https://boot.dev"'
		)

	def test_props_to_html_multiple_props(self):
		node = HTMLNode(
			tag="a", 
			props={
				"href": "https://boot.dev", 
				"target": "_blank"
			}
		)


class TestLeafNode(unittest.TestCase):

	def test_leaf_to_html_p(self):
		node = LeafNode("p", "Hello, world!")
		self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

	def test_leaf_to_html_with_props(self):
		node = LeafNode(
			"a", 
			"Click me", 
			{"href": "https://boot.dev"}
		)
		self.assertEqual(
			node.to_html(), 
			'<a href="https://boot.dev">Click me</a>'
		)

	def test_leaf_to_html_raw_text(self):
		node = LeafNode(None, "Just plain text")
		self.assertEqual(node.to_html(), "Just plain text")

	def test_leaf_raises_if_value_none(self):
		with self.assertRaises(ValueError):
			LeafNode("p", None)

	def test_leaf_to_html_raises_if_value_none(self):
		node = LeafNode("p", "valid")
		node.value = None
		with self.assertRaises(ValueError):
			node.to_html()

	def test_leaf_children_are_none(self):
		node = LeafNode("p", "Hello")
		self.assertIsNone(node.children)

class TestParentNode(unittest.TestCase):

	def test_parent_single_child(self):
		node = ParentNode(
			"div", 
			[LeafNode("p", "Hello")]
		)
		self.assertEqual(
			node.to_html(), 
			"<div><p>Hello</p></div>"
		)

	def test_parent_multiple_children(self):
		node = ParentNode(
			"div", 
			[
				LeafNode("p", "Hello"), 
				LeafNode("p", "World")
			]
		)
		self.assertEqual(
			node.to_html(),
			"<div><p>Hello</p><p>World</p></div>"
		)

	def test_parent_nested_parents(self):
		node = ParentNode(
			"div", 
			[
				ParentNode(
					"section", 
					[
						LeafNode("p", "Nested text")
					]
				)
			]
		)
		self.assertEqual(
			node.to_html(),
			"<div><section><p>Nested text</p></section></div>"
		)

	def test_parent_with_props(self):
		node = ParentNode(
			"div", 
			[LeafNode("p", "Hello")], 
			props={"class": "container"}
		)
		self.assertEqual(
			node.to_html(), 
			'<div class="container"><p>Hello</p></div>'
		)

	def test_parent_raises_if_no_tag(self):
		with self.assertRaises(ValueError):
			ParentNode(None, [LeafNode("p", "Hello")])

	def test_parent_raises_if_children_none(self):
		with self.assertRaises(ValueError):
			ParentNode("div", None)

	def test_parent_raises_if_children_etmpty(self):
		node = ParentNode("div", [])
		with self.assertRaises(ValueError):
			node.to_html()

class TestTextNodeToHTMLNode(unittest.TestCase):

	def test_text_node_text(self):
		text_node = TextNode("Hello", TextType.TEXT)
		html_node = text_node_to_html_node(text_node)
		self.assertEqual(html_node.to_html(), "Hello")

	def test_text_node_bold(self):
		text_node = TextNode("Italic", TextType.ITALIC)
		html_node = text_node_to_html_node(text_node)
		self.assertEqual(html_node.to_html(), "<i>Italic</i>")

	def test_text_node_code(self):
		text_node = TextNode("print('hi')", TextType.CODE)
		html_node = text_node_to_html_node(text_node)
		self.assertEqual(html_node.to_html(), "<code>print('hi')</code>")

	def text_text_node_link(self):
		text_node = TextNode(
			"Click me", 
			TextType.LINK, 
			"https://boot.dev"
		)
		html_node = text_node_to_html_node(text_node)
		self.assertEqual(
			html_node.to_html(), 
			'<a href="https://boot.dev">Click me</a>'
		)

	def test_text_node_image(self):
		text_node = TextNode(
			"Alt text",
			TextType.IMAGE, 
			"image.png"
		)
		html_node = text_node_to_html_node(text_node)
		self.assertEqual(
			html_node.to_html(), 
			'<img src="image.png" alt="Alt text"></img>'
		)

	def test_link_raises_without_url(self):
		text_node = TextNode("Click", TextType.LINK)
		with self.assertRaises(ValueError):
			text_node_to_html_node(text_node)

	def test_image_raises_without_url(self):
		text_node = TextNode("Alt", TextType.IMAGE)
		with self.assertRaises(ValueError):
			text_node_to_html_node(text_node)



if __name__ == "__main__":
	unittest.main()
