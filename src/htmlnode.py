from textnode import TextNode, TextType

class HTMLNode:
	def __init__(self, tag=None, value=None, children=None, props=None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImplementedError("Subclasses must implement to_html()")

	def props_to_html(self):
		if not self.props:
			return ""

		props_str = ""
		for key, value in self.props.items():
			props_str += f' {key}="{value}"'

		return props_str

	def __repr__(self):
		return (
			f"HTMLNode("
			f"tag={self.tag!r}, "
			f"value={self.value!r}, "
			f"children={self.children!r}, "
			f"props={self.props!r}"
			f")"
		)

class LeafNode(HTMLNode):
	def __init__(self, tag, value, props=None):
		if value is None:
			raise ValueError("LeafNode must have a value")
		super().__init__(tag=tag, value=value, children=None, props=props)

	def to_html(self):
		if self.value is None:
			raise ValueError("LeafNode must have a value")

		if self.tag is None:
			return self.value

		return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"



class ParentNode(HTMLNode):
	def __init__(self, tag, children, props=None):
		if tag is None:
			raise ValueError("ParentNode must have a tag")
		if children is None:
			raise ValueError("ParentNode must have children")

		super().__init__(tag=tag, value=None, children=children, props=props)

	def to_html(self):
		if self.tag is None:
			raise ValueError("ParentNode must have a tag")

		if not self.children:
			raise ValueError("ParentNode must have at least one child")

		children_html = ""
		for child in self.children:
			children_html += child.to_html()

		return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

def text_node_to_html_node(text_node):
	if text_node.text_type == TextType.TEXT:
		return LeafNode(None, text_node.text)

	if text_node.text_type == TextType.BOLD:
		return LeafNode("b", text_node.text)

	if text_node.text_type == TextType.ITALIC:
		return LeafNode("i", text_node.text)

	if text_node.text_type == TextType.CODE:
		return LeafNode("code", text_node.text)

	if text_node.text_type == TextType.LINK:
		if text_node.url is None:
			raise ValueError("Link text node must have a URL")
		return LeafNode(
			"a", 
			text_node.text, 
			{"href": text_node.url}
		)

	if text_node.text_type == TextType.IMAGE:
		if text_node.url is None:
			raise ValueError("IMAGE text node must have a URL")
		return LeafNode(
			"img", 
			"", 
			{"src": text_node.url, "alt": text_node.text}
		)

	raise ValueError(f"Unsupported TextType: {text_node.text_type}")
