from rest_framework.permissions import BasePermission

from users.utils import get_user_roles


class UserCanCreateHits(BasePermission):
    """
    Allows hits creation only to managers and superusers
    """

    def has_permission(self, request, view):
        user = request.user
        roles = get_user_roles(user)
        return "manager" in roles or user.is_superuser
