from cuser.models import CUser
from rest_framework.permissions import BasePermission

from users.models import ManagerUser
from users.utils import is_manager


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
            is_manager(request.user)
            and ManagerUser.objects.filter(
                user=CUser.objects.get(email=request.data["assigned_to"]),
                manager=request.user,
            ).first()
        ):  # Check that assigned user is a lackey of logged user
            return True

        return False

    def has_permission(self, request, view):
        self.can_create_hit_for_assigned_user(request)
        user = request.user
        return (
            is_manager(user) or user.is_superuser
        ) and self.can_create_hit_for_assigned_user(request)


class UserCanAssignHits(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if "assigned_to" not in request.data:
            return True

        if request.data["assigned_to"] == user.email:
            return False

        if user.is_superuser:
            return True

        if (
            is_manager(request.user)
            and ManagerUser.objects.filter(
                user=CUser.objects.get(email=request.data["assigned_to"]),
                manager=request.user,
            ).first()
        ):  # Check that assigned user is a lackey of logged user
            return True

        return False
