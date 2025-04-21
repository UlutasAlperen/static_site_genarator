import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def text_props_to_html(self):
        node = HTMLNode("p","lorem",props={"href":"cart"})
        expected = ' href="cart"' 
        self.assertEqual(expected,node.props_to_html())


    def test_props_to_html_with_multiple_attrs(self):
        node = HTMLNode("p","lorem",props={"href":"cart","cart":"curt"})
        expected = ' href="cart" cart="curt"' 
        self.assertEqual(node.props_to_html(),expected)


    def text_empty_props(self):
        node = HTMLNode("p","",props= {})
        self.assertEqual("",node.props_to_html())

    def test_repr_output(self):
        node = HTMLNode("p", "Hello", props={"class": "text-bold"})
        result = repr(node)
        self.assertIn("tag=p", result)
        self.assertIn("value=Hello", result)
        self.assertIn("'class': 'text-bold'", result)

   


if __name__ == "__main__":
    unittest.main()
