from cuser.models import CUser as User, Group
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from hitman.utils.viewset_mixin import PermissionByActionMixin
from users.permissions import UserCanViewUsers
from users.serializers import (
    UserSerializer,
    CreateUserSerializer,
    UserProfileSerializer,
)
from users.utils import get_user_roles, is_manager


class UserViewSet(PermissionByActionMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes_by_action = {
        "create": [AllowAny],
        "list": [IsAuthenticated, UserCanViewUsers],
    }

    def get_queryset(self):
        if is_manager(self.request.user):
            return self.queryset.filter(user__manager_id=self.request.user.id).all()

        return super(UserViewSet, self).get_queryset()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateUserSerializer

        return self.serializer_class

    def create(self, request, *args, **kwargs):
        create_user_serializer = CreateUserSerializer(data=request.data)

        if not create_user_serializer.is_valid():
            return Response("Bad request", status.HTTP_400_BAD_REQUEST)

        cleaned_data = create_user_serializer.data
        user_exists = User.objects.filter(email=cleaned_data["email"]).first()
        if user_exists:
            return Response(
                {"detail": "A user with this email already exists"},
                status.HTTP_409_CONFLICT,
            )
        user = User(
            email=cleaned_data["email"],
            password=make_password(cleaned_data["password"]),
        )
        user.save()

        default_role = Group.objects.get(name="hitman")
        default_role.user_set.add(user)

        return Response(self.serializer_class(user).data, status.HTTP_201_CREATED)

    @action(methods=["GET"], detail=False, description="Retrieves the user's profile")
    def profile(self, request):
        profile = {
            "email": request.user.email,
            "roles": get_user_roles(request.user),
            "is_super_user": request.user.is_superuser,
        }
        profile_serializer = UserProfileSerializer(data=profile)

        if not profile_serializer.is_valid():
            raise Exception(
                "INVALID_USER_PROFILE"
            )  # Todo add middleware to handle custom exceptions

        return Response(data=profile_serializer.data)
