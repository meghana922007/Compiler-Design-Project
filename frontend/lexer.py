# frontend/lexer.py

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
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.type}:{self.value}"

def lex(file_path):
    tokens = []
    with open(file_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Add spaces around special symbols for splitting
        line = line.replace("{", " { ").replace("}", " } ") \
                   .replace("=", " = ").replace(",", " , ") \
                   .replace("[", " [ ").replace("]", " ] ")
        parts = line.split()

        for part in parts:
            if part == "role":
                tokens.append(Token(TOKEN_ROLE, part))
            elif part == "user":
                tokens.append(Token(TOKEN_USER, part))
            elif part == "extends":
                tokens.append(Token(TOKEN_EXTENDS, part))
            elif part == "{":
                tokens.append(Token(TOKEN_LBRACE, part))
            elif part == "}":
                tokens.append(Token(TOKEN_RBRACE, part))
            elif part == "=":
                tokens.append(Token(TOKEN_EQUALS, part))
            elif part == "permissions":
                tokens.append(Token(TOKEN_PERMISSIONS, part))
            elif part == "roles":
                tokens.append(Token(TOKEN_ROLES, part))
            elif part == "[":
                tokens.append(Token(TOKEN_LBRACKET, part))
            elif part == "]":
                tokens.append(Token(TOKEN_RBRACKET, part))
            elif part == ",":
                tokens.append(Token(TOKEN_COMMA, part))
            else:
                tokens.append(Token(TOKEN_IDENTIFIER, part))

    tokens.append(Token(TOKEN_EOF, None))
    return tokens
