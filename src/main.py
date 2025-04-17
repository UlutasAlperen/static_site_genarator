from textnode import TextNode
from textnode import TextType

def main():
    my_var = TextNode("This is some anchor text", TextType.link , "https://www.boot.dev")
    print(my_var)
    

main()
