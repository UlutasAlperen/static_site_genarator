from textnode import TextType,TextNode

def main():
    my_var = TextNode("This is some anchor text", TextType.LINK , "https://www.boot.dev")
    print(my_var)
    

main()
