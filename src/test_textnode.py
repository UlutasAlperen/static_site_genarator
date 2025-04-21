import unittest
from textnode import TextNode,TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is not a node", TextType.BOLD)
        node4 = TextNode("This is not a node", TextType.TEXT)
        node5 = TextNode("This is not a node", TextType.TEXT)
        self.assertEqual(node, node2)
        self.assertNotEqual(node2,node3)
        self.assertNotEqual(node,node5)
        self.assertEqual(node5, node4)




if __name__ == "__main__":
    unittest.main()
