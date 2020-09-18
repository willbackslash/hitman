from rest_framework.permissions import BasePermission

from users.utils import is_manager


class UserCanViewUsers(BasePermission):
    """
    Allows get users list only to managers and superusers
    """

    def has_permission(self, request, view):
        user = request.user
        return is_manager(user) or user.is_superuser
