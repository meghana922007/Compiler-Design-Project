from core.symbol_table import SymbolTable

class Role:
    def __init__(self, name):
        self.name = name
        self.permissions = []
        self.parents = []

class User:
    def __init__(self, name):
        self.name = name
        self.roles = []

def parse_policy(file_path):
    table = SymbolTable()
    current_block = None

    with open(file_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("role "):
            parts = line.split()
            role_name = parts[1]
            role = Role(role_name)

            if "extends" in line:
                role.parents = [parts[3]] 
            table.add_role(role)
            current_block = role
            continue

        if line.startswith("user "):
            user_name = line.split()[1]
            user = User(user_name)
            table.add_user(user)
            current_block = user
            continue

        if current_block and "=" in line:
            key, value = line.split("=")
            key = key.strip()
            value = value.strip().strip("[]")  
            items = [v.strip() for v in value.split(",") if v.strip()]

            if isinstance(current_block, Role) and key == "permissions":
                current_block.permissions.extend(items)
            elif isinstance(current_block, User) and key == "roles":
                current_block.roles.extend(items)

    return table
