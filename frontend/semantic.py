def perform_semantic_analysis(table):
    errors = []

    for role_name, line in table.duplicate_roles:
        errors.append(
            f"[SEMANTIC ERROR] Line {line}: Duplicate role '{role_name}'"
        )

    for user_name, line in table.duplicate_users:
        errors.append(
            f"[SEMANTIC ERROR] Line {line}: Duplicate user '{user_name}'"
        )

    for role_name, role_obj in table.roles.items():
        for parent in role_obj.parents:
            if parent not in table.roles:
                errors.append(
                    f"[SEMANTIC ERROR] Line {role_obj.line}: "
                    f"Role '{role_name}' extends undefined role '{parent}'"
                )

    for user_name, user_obj in table.users.items():
        for role in user_obj.roles:
            if role not in table.roles:
                errors.append(
                    f"[SEMANTIC ERROR] Line {user_obj.line}: "
                    f"User '{user_name}' references undefined role '{role}'"
                )

    for role_name, role_obj in table.roles.items():
        if not role_obj.permissions:
            errors.append(
                f"[SEMANTIC ERROR] Line {role_obj.line}: "
                f"Role '{role_name}' has no permissions defined"
            )

    visited = set()
    stack = set()

    def dfs(role_name):
        if role_name in stack:
            errors.append(
                f"[SEMANTIC ERROR] Circular inheritance detected involving role '{role_name}'"
            )
            return

        if role_name in visited:
            return

        visited.add(role_name)
        stack.add(role_name)

        role_obj = table.roles.get(role_name)
        if role_obj:
            for parent in role_obj.parents:
                dfs(parent)

        stack.remove(role_name)

    for role_name in table.roles:
        dfs(role_name)

    return errors