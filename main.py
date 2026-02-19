from frontend.lexer import lex
from frontend.parser import parse_policy
from frontend.semantic import check_semantics

DSL_FILE = "dsl/policy.rbac"

PRINT_TOKENS = False     
PRINT_AST = True        

print("*** RBAC POLICY DSL COMPILER ***\n")

# Phase 1: Lexical Analysis
tokens = lex(DSL_FILE)
print("[Phase 1] Lexical Analysis")
print(f"Tokens generated: {len(tokens)-1} (excluding EOF)\n")

if PRINT_TOKENS:
    print("Tokens (with line numbers):")
    for t in tokens[:-1]:  # skip EOF
        print(f"  {t.type}:{t.value} (line {t.line})")
    print()

# Phase 2: Parsing & Symbol Table Construction
print("[Phase 2] Parsing & Symbol Table Construction")
table, ast_nodes, syntax_errors = parse_policy(DSL_FILE)
print(f"Roles Loaded: {len(table.roles)}")
print(f"Users Loaded: {len(table.users)}\n")

# Print Symbol Table
print("[Symbol Table] Roles:")
for r in table.roles.values():
    print(f"  Role: {r.name}")
    print(f"    Permissions: {', '.join(r.permissions) if r.permissions else 'None'}")
    print(f"    Inherits: {', '.join(r.parents) if r.parents else 'None'}")

print("\n[Symbol Table] Users:")
for u in table.users.values():
    print(f"  User: {u.name}")
    print(f"    Assigned Roles: {', '.join(u.roles) if u.roles else 'None'}")

# Function to print AST branches
def print_ast_branch(node, indent="", last=True):
    branch = "└── " if last else "├── "
    print(indent + branch + f"{node.type}: {node.name}")

    if node.type == "Role":
        if node.permissions:
            print(indent + ("    " if last else "│   ") + f"Permissions: {', '.join(node.permissions)}")
        if node.parents:
            print(indent + ("    " if last else "│   ") + f"Inherits: {', '.join(node.parents)}")
    elif node.type == "User":
        if node.roles:
            print(indent + ("    " if last else "│   ") + f"Assigned Roles: {', '.join(node.roles)}")

    child_count = len(getattr(node, "children", []))
    for idx, child in enumerate(getattr(node, "children", [])):
        print_ast_branch(child, indent + ("    " if last else "│   "), idx == child_count - 1)

# Print AST Tree
if PRINT_AST:
    print("\n[AST Tree]")
    for idx, node in enumerate(ast_nodes):
        print_ast_branch(node, "", idx == len(ast_nodes)-1)

# Print Syntax Errors
if syntax_errors:
    print("\n[Syntax Errors]")
    for e in syntax_errors:
        print(e)
    print(f"\nSyntax errors also saved to 'syntax_errors.txt'")
else:
    print("\nNo syntax errors detected")

# Phase 3: Semantic Validation
print("\n[Phase 3] Semantic Validation")
sem_results = check_semantics(table)
if sem_results:
    for msg in sem_results:
        print(msg)
else:
    print("No semantic issues detected")
