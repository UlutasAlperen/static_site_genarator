class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.childeren = children
        self.props = props


    def to_html(self):
        raise NotImplementedError("not impelemented")


    def props_to_html(self):
        if not isinstance(self.props,dict):
            return ""
        if isinstance(self.props,dict):
            new_str = ""
            for key,value in self.props.items():
                new_str += ' ' + key + '=' + '"' + value + '"'
            return new_str
    
    def __repr__(self):
        return f"HtmlNode(tag={self.tag},value={self.value},children={self.childeren},props={self.props})"


