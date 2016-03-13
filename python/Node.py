class Node:
    def __init__(self, token=None):
        self.token = token
        self.level = 0
        self.children = []  # a list of my children
    
    def add(self, token):
        """
        make a node out of a token and add it to self.children
        """
        self.addNode(  Node(token) )
        
    def addNode(self, node):
        """
        add a node to self.children
        """
        node.level = self.level + 1
        self.children.append(node)
        
    def toString(self):
        s = "    " * self.level
        
        if self.token == None: s += "ROOT\n"
        else: s +=  self.token.cargo + "\n"
            
        for child in self.children:
            s += child.toString()
        return s