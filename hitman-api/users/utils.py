from hitman.constants import USER_ROLE_HITMAN, USER_ROLE_MANAGER


def flat_user_roles(user_roles):
    return [role["name"] for role in user_roles]


def is_manager(user):
    roles = flat_user_roles(get_user_roles(user))
    return USER_ROLE_MANAGER in roles


def is_hitman(user):
    roles = flat_user_roles(get_user_roles(user))
    return USER_ROLE_HITMAN in roles


def get_user_roles(user):
    return [{"id": group.id, "name": group.name} for group in user.groups.all()]
