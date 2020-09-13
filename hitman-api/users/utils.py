def get_user_roles(user):
    return [group.name for group in user.groups.all()]
