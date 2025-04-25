import unittest
from htmlnode import HTMLNode, LeafNode,ParentNode,text_node_to_html_node
from textnode import TextNode,TextType


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("p","lorem",props={"href":"cart"})
        expected = ' href="cart"' 
        self.assertEqual(expected,node.props_to_html())


    def test_props_to_html_with_multiple_attrs(self):
        node = HTMLNode("p","lorem",props={"href":"cart","cart":"curt"})
        expected = ' href="cart" cart="curt"' 
        self.assertEqual(node.props_to_html(),expected)


    def test_empty_props(self):
        node = HTMLNode("p","",props= {})
        self.assertEqual("",node.props_to_html())

    def test_repr_output(self):
        node = HTMLNode("p", "Hello", props={"class": "text-bold"})
        result = repr(node)
        self.assertIn("tag=p", result)
        self.assertIn("value=Hello", result)
        self.assertIn("'class': 'text-bold'", result)


    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(),"<p>Hello, world!</p>")
        
    def test_leaf_to_html_2(self):
        node = LeafNode("p", "Hello, world!",props={"href":"cart-curt"})
        self.assertEqual(node.to_html(),'<p href="cart-curt">Hello, world!</p>')

    def test_leaf_to_html_3(self):
        node = LeafNode(None, "Hello, world!",)
        self.assertEqual(node.to_html(),"Hello, world!")
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

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        # Test converting a LINK type node
        node = TextNode("Click me", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click me")
        self.assertEqual(html_node.props, {"href": "https://example.com"})
        
    def test_image(self):
        # Test converting an IMAGE type node
        node = TextNode("Alt text for image", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.png", "alt": "Alt text for image"})
        

if __name__ == "__main__":
    unittest.main()
