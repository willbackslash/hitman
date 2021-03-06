from cuser.models import CUser as User, Group, CUser
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from hitman.constants import USER_ROLE_HITMAN, USER_ROLE_MANAGER
from hitman.utils.viewset_mixin import PermissionByActionMixin
from users.models import ManagerUser
from users.permissions import UserCanViewUsers
from users.serializers import (
    UserSerializer,
    CreateUserSerializer,
    UserProfileSerializer,
    UpdateUserSerializer,
)
from users.utils import get_user_roles, is_manager


class UserViewSet(PermissionByActionMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes_by_action = {
        "create": [AllowAny],
        "list": [IsAuthenticated, UserCanViewUsers],
        "update": [IsAuthenticated],
    }
    http_method_names = ["get", "post", "put", "options"]

    def get_queryset(self):
        if is_manager(self.request.user):
            return self.queryset.filter(user__manager_id=self.request.user.id).all()

        return super(UserViewSet, self).get_queryset()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateUserSerializer
        if self.action == "update":
            return UpdateUserSerializer

        return self.serializer_class

    @staticmethod
    def create_user(cleaned_data):
        user = User(
            first_name=cleaned_data["first_name"],
            last_name=cleaned_data["last_name"],
            email=cleaned_data["email"],
            password=make_password(cleaned_data["password"]),
        )
        user.save()
        return user

    @staticmethod
    def set_default_user_role(user):
        default_role = Group.objects.get(name=USER_ROLE_HITMAN)
        default_role.user_set.add(user)

    def create(self, request, *args, **kwargs):
        create_user_serializer = CreateUserSerializer(data=request.data)

        if not create_user_serializer.is_valid():
            return Response(
                {"detail": create_user_serializer.errors}, status.HTTP_400_BAD_REQUEST
            )

        cleaned_data = create_user_serializer.data
        user_exists = User.objects.filter(email=cleaned_data["email"]).first()
        if user_exists:
            return Response(
                {"detail": "A user with this email already exists"},
                status.HTTP_409_CONFLICT,
            )
        user = self.create_user(cleaned_data)
        self.set_default_user_role(user)

        return Response(self.serializer_class(user).data, status.HTTP_201_CREATED)

    @action(methods=["GET"], detail=False, description="Retrieves the user's profile")
    def profile(self, request):
        profile = {
            "email": request.user.email,
            "roles": get_user_roles(request.user),
            "is_superuser": request.user.is_superuser,
        }
        profile_serializer = UserProfileSerializer(data=profile)

        if not profile_serializer.is_valid():
            return Response(
                {"detail": "Invalid user profile"}, status=status.HTTP_403_FORBIDDEN
            )

        return Response(data=profile_serializer.data)

    @staticmethod
    def deactivate_user(user_to_update):
        user_to_update.is_active = False
        user_to_update.save()

    @staticmethod
    def update_managed_users(user_to_update, cleaned_data):
        managed_users_ids = [user["id"] for user in cleaned_data["managed_users"]]
        current_managed_user_ids = [
            managed_user.user.id
            for managed_user in ManagerUser.objects.filter(manager=user_to_update).all()
        ]
        managed_users_to_add = list(
            set(managed_users_ids) - set(current_managed_user_ids)
        )
        managed_users_to_remove = list(
            set(current_managed_user_ids) - set(managed_users_ids)
        )
        for user_to_add in managed_users_to_add:
            ManagerUser(
                manager=user_to_update, user=CUser.objects.get(pk=user_to_add)
            ).save()

        if len(managed_users_to_remove) > 0:
            ManagerUser.objects.filter(
                manager=user_to_update, user_id__in=managed_users_to_remove
            ).delete()

    @staticmethod
    def update_user_role(user_to_update):
        number_managed_users = ManagerUser.objects.filter(
            manager=user_to_update
        ).count()

        if not user_to_update.is_superuser:
            if number_managed_users > 0:
                Group.objects.get(name=USER_ROLE_MANAGER).user_set.add(user_to_update)
                Group.objects.get(name=USER_ROLE_HITMAN).user_set.remove(user_to_update)
            else:
                Group.objects.get(name=USER_ROLE_MANAGER).user_set.remove(
                    user_to_update
                )
                Group.objects.get(name=USER_ROLE_HITMAN).user_set.add(user_to_update)

    def update(self, request, *args, **kwargs):
        update_user_serializer = UpdateUserSerializer(data=request.data)

        if not update_user_serializer.is_valid():
            return Response(
                {"detail": update_user_serializer.errors}, status.HTTP_400_BAD_REQUEST
            )

        user_to_update = CUser.objects.filter(pk=kwargs["pk"]).first()
        cleaned_data = update_user_serializer.data

        if not user_to_update:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if not user_to_update.is_active and cleaned_data["is_active"]:
            return Response(
                {"detail": "You can't reactivate users"},
                status=status.HTTP_403_FORBIDDEN,
            )

        if user_to_update.is_active and cleaned_data["is_active"] == False:
            self.deactivate_user(user_to_update)

        if (
            "managed_users" in cleaned_data
            and cleaned_data["managed_users"] is not None
        ):
            self.update_managed_users(user_to_update, cleaned_data)

        self.update_user_role(user_to_update)

        return Response(
            self.serializer_class(user_to_update).data,
            status.HTTP_200_OK,
        )
