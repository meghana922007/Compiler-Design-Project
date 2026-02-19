class SymbolTable:
    def __init__(self):
        self.roles = {}
        self.users = {}

    def add_role(self, role):
        self.roles[role.name] = role

    def add_user(self, user):
        self.users[user.name] = user
