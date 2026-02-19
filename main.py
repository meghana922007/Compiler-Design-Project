from frontend.parser import parse_policy
from frontend.semantic import check_semantics

print("*** RBAC POLICY DSL COMPILER ***\n")

print("[Phase 1] Parsing")
table = parse_policy("dsl/policy.rbac")
print("DSL parsed successfully\n")

print("[Phase 2] Symbol Table Construction")
print(f"Roles Loaded: {len(table.roles)}")
print(f"Users Loaded: {len(table.users)}\n")

print("[Symbol Table] Roles:")
for r in table.roles.values():
    print(f"  Role: {r.name}")
    print(f"    Permissions: {', '.join(r.permissions)}")
    print(f"    Inherits: {', '.join(r.parents) if r.parents else 'None'}")

print("\n[Symbol Table] Users:")
for u in table.users.values():
    print(f"  User: {u.name}")
    print(f"    Assigned Roles: {', '.join(u.roles)}")
print()  

print("[Phase 3] Semantic Validation")
results = check_semantics(table)
if results:
    for msg in results:
        print(msg)
else:
    print("No semantic issues detected")

print("\nFrontend phase completed successfully")
