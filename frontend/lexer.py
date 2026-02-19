TOKEN_ROLE = "ROLE"
TOKEN_USER = "USER"
TOKEN_IDENTIFIER = "IDENTIFIER"
TOKEN_EXTENDS = "EXTENDS"
TOKEN_LBRACE = "LBRACE"
TOKEN_RBRACE = "RBRACE"
TOKEN_EQUALS = "EQUALS"
TOKEN_PERMISSIONS = "PERMISSIONS"
TOKEN_ROLES = "ROLES"
TOKEN_COMMA = "COMMA"
TOKEN_LBRACKET = "LBRACKET"
TOKEN_RBRACKET = "RBRACKET"
TOKEN_EOF = "EOF"

class Token:
    def __init__(self, type_, value, line=0):
        self.type = type_
        self.value = value
        self.line = line

    def __repr__(self):
        return f"{self.type}:{self.value}"

def lex(file_path):
    tokens = []
    with open(file_path, "r") as f:
        lines = f.readlines()

    for idx, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        line = line.replace("{", " { ").replace("}", " } ") \
                   .replace("=", " = ").replace(",", " , ") \
                   .replace("[", " [ ").replace("]", " ] ")
        parts = line.split()

        for part in parts:
            if part == "role":
                tokens.append(Token(TOKEN_ROLE, part, idx))
            elif part == "user":
                tokens.append(Token(TOKEN_USER, part, idx))
            elif part == "extends":
                tokens.append(Token(TOKEN_EXTENDS, part, idx))
            elif part == "{":
                tokens.append(Token(TOKEN_LBRACE, part, idx))
            elif part == "}":
                tokens.append(Token(TOKEN_RBRACE, part, idx))
            elif part == "=":
                tokens.append(Token(TOKEN_EQUALS, part, idx))
            elif part == "permissions":
                tokens.append(Token(TOKEN_PERMISSIONS, part, idx))
            elif part == "roles":
                tokens.append(Token(TOKEN_ROLES, part, idx))
            elif part == "[":
                tokens.append(Token(TOKEN_LBRACKET, part, idx))
            elif part == "]":
                tokens.append(Token(TOKEN_RBRACKET, part, idx))
            elif part == ",":
                tokens.append(Token(TOKEN_COMMA, part, idx))
            else:
                tokens.append(Token(TOKEN_IDENTIFIER, part, idx))

    tokens.append(Token(TOKEN_EOF, None, idx))
    return tokens
