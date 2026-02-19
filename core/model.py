class Role:
    def __init__(self, name):
        self.name = name
        self.permissions = set()
        self.parents = []
        self.children = [] 

class User:
    def __init__(self, name):
        self.name = name
        self.roles = []
        self.children = [] 

class ASTNode:
    def __init__(self, type_, name):
        self.type = type_  
        self.name = name
        self.permissions = []
        self.parents = []
        self.roles = []
        self.children = []
