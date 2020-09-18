def is_manager(user):
    roles = get_user_roles(user)
    return "manager" in roles


def get_user_roles(user):
    return [group.name for group in user.groups.all()]
