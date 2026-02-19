from core.symbol_table import SymbolTable
from core.model import Role, User, ASTNode
from frontend.lexer import lex, TOKEN_ROLE, TOKEN_USER, TOKEN_IDENTIFIER, TOKEN_EXTENDS, TOKEN_LBRACE, TOKEN_RBRACE, TOKEN_EQUALS, TOKEN_PERMISSIONS, TOKEN_ROLES, TOKEN_LBRACKET, TOKEN_RBRACKET, TOKEN_COMMA, TOKEN_EOF

def parse_policy(file_path):
    tokens = lex(file_path)
    table = SymbolTable()
    ast_nodes = []
    syntax_errors = []

    i = 0
    n = len(tokens)

    def current():
        return tokens[i] if i < n else None

    def advance():
        nonlocal i
        i += 1
        return current()

    while i < n:
        tok = current()
        if tok.type == TOKEN_EOF:
            break

        if tok.type == TOKEN_ROLE:
            try:
                advance()
                role_name = current().value
                role = Role(role_name)
                node = ASTNode("Role", role_name)
                advance()

                if current().type == TOKEN_EXTENDS:
                    advance()
                    parent_name = current().value
                    role.parents.append(parent_name)
                    node.parents.append(parent_name)
                    advance()

                if current().type != TOKEN_LBRACE:
                    syntax_errors.append(f"[SYNTAX ERROR] Line {tok.line}: Role '{role_name}' missing '{{'")
                    while current().type not in [TOKEN_LBRACE, TOKEN_EOF]:
                        advance()
                advance()

                while current().type != TOKEN_RBRACE and current().type != TOKEN_EOF:
                    if current().type == TOKEN_PERMISSIONS:
                        advance()
                        if current().type != TOKEN_EQUALS:
                            syntax_errors.append(f"[SYNTAX ERROR] Line {current().line}: Role '{role_name}' permissions missing '='")
                        else:
                            advance()
                        if current().type != TOKEN_LBRACKET:
                            syntax_errors.append(f"[SYNTAX ERROR] Line {current().line}: Role '{role_name}' permissions missing '['")
                        else:
                            advance()
                        perms = []
                        while current().type not in [TOKEN_RBRACKET, TOKEN_EOF]:
                            if current().type == TOKEN_IDENTIFIER:
                                perms.append(current().value)
                            advance()
                        role.permissions.update(perms)
                        node.permissions.extend(perms)
                        if current().type == TOKEN_RBRACKET:
                            advance()
                    else:
                        syntax_errors.append(f"[SYNTAX ERROR] Line {current().line}: Role '{role_name}' unexpected token '{current().value}'")
                        advance()
                if current().type == TOKEN_RBRACE:
                    advance()
                table.add_role(role)
                ast_nodes.append(node)
            except Exception as e:
                syntax_errors.append(f"[FATAL ERROR] Line {tok.line}: Parsing Role '{role_name}': {e}")
            continue

        elif tok.type == TOKEN_USER:
            try:
                advance()
                user_name = current().value
                user = User(user_name)
                node = ASTNode("User", user_name)
                advance()

                if current().type != TOKEN_LBRACE:
                    syntax_errors.append(f"[SYNTAX ERROR] Line {tok.line}: User '{user_name}' missing '{{'")
                    while current().type not in [TOKEN_LBRACE, TOKEN_EOF]:
                        advance()
                advance()

                while current().type != TOKEN_RBRACE and current().type != TOKEN_EOF:
                    if current().type == TOKEN_ROLES:
                        advance()
                        if current().type != TOKEN_EQUALS:
                            syntax_errors.append(f"[SYNTAX ERROR] Line {current().line}: User '{user_name}' roles missing '='")
                        else:
                            advance()
                        if current().type != TOKEN_LBRACKET:
                            syntax_errors.append(f"[SYNTAX ERROR] Line {current().line}: User '{user_name}' roles missing '['")
                        else:
                            advance()
                        roles_list = []
                        while current().type not in [TOKEN_RBRACKET, TOKEN_EOF]:
                            if current().type == TOKEN_IDENTIFIER:
                                roles_list.append(current().value)
                            advance()
                        user.roles.extend(roles_list)
                        node.roles.extend(roles_list)
                        if current().type == TOKEN_RBRACKET:
                            advance()
                    else:
                        syntax_errors.append(f"[SYNTAX ERROR] Line {current().line}: User '{user_name}' unexpected token '{current().value}'")
                        advance()
                if current().type == TOKEN_RBRACE:
                    advance()
                table.add_user(user)
                ast_nodes.append(node)
            except Exception as e:
                syntax_errors.append(f"[FATAL ERROR] Line {tok.line}: Parsing User '{user_name}': {e}")
            continue

        else:
            syntax_errors.append(f"[SYNTAX ERROR] Line {tok.line}: Unexpected token '{tok.value}'")
            advance()

    # Save syntax errors to a file
    if syntax_errors:
        with open("syntax_errors.txt", "w") as f:
            for err in syntax_errors:
                f.write(err + "\n")

    return table, ast_nodes, syntax_errors
