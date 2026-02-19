class Role:
    def __init__(self, name):
        self.name = name
        self.permissions = set()
        self.parents = []

class User:
    def __init__(self, name):
        self.name = name
        self.roles = []
