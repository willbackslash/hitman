from cuser.models import CUser
from rest_framework.permissions import BasePermission

from users.models import ManagerUser
from users.utils import get_user_roles


class UserCanCreateHits(BasePermission):
    """
    Allows hits creation only to managers and superusers
    """

    def can_create_hit_for_assigned_user(self, request):
        if not "assigned_to" in request.data:
            return False

        if request.data["assigned_to"] == request.user.email:
            return False

        if request.user.is_superuser:
            return True

        if (
            self.is_manager(request.user)
            and ManagerUser.objects.filter(
                user=CUser.objects.get(email=request.data["assigned_to"]),
                manager=request.user,
            ).first()
        ):  # Check that assigned user is a lackey of logged user
            return True

        return False

    def is_manager(self, user):
        roles = get_user_roles(user)
        return "manager" in roles

    def has_permission(self, request, view):
        self.can_create_hit_for_assigned_user(request)
        user = request.user
        return (
            self.is_manager(user) or user.is_superuser
        ) and self.can_create_hit_for_assigned_user(request)
