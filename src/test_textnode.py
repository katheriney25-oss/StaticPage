import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node, node2)

	def test_noteq_diff_text(self):
		node = TextNode("This is not a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertNotEqual(node, node2)

	def test_equ_both_urls_none(self):
		node = TextNode("Link", TextType.LINK, None)
		node2 = TextNode("Link", TextType.LINK, None)
		self.assertEqual(node, node2)

	def test_not_eq_urlvnone(self):
		node = TextNode("Link", TextType.LINK, None)
		node2 = TextNode("Link", TextType.LINK, "https://boot.dev")
		self.assertNotEqual(node, node2)

	def test_not_eq_different_texttype(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.ITALIC)
		self.assertNotEqual(node, node2)




if __name__ == "__main__":
	unittest.main()

