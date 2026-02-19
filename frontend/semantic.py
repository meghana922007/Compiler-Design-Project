def check_semantics(table):
    messages = []

    # Check undefined parent roles
    for role in table.roles.values():
        for parent in role.parents:
            if parent not in table.roles:
                messages.append(
                    f"[WARNING] Role '{role.name}' inherits undefined role '{parent}'"
                )

    # Check roles with no permissions
    for role in table.roles.values():
        if len(role.permissions) == 0:
            messages.append(
                f"[INFO] Role '{role.name}' has no permissions assigned"
            )

    return messages
