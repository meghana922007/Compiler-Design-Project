def check_semantics(table):
    messages = []

    for role in table.roles.values():
        for parent in role.parents:
            if parent not in table.roles:
                messages.append(f"[WARNING] Role '{role.name}' inherits undefined role '{parent}'")

    for role in table.roles.values():
        if not role.permissions:
            messages.append(f"[INFO] Role '{role.name}' has no permissions assigned")

    for user in table.users.values():
        if not user.roles:
            messages.append(f"[INFO] User '{user.name}' has no roles assigned")

    return messages
