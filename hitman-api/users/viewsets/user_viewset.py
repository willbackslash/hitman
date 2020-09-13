from cuser.models import CUser as User
from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.serializers import (
    UserSerializer,
    CreateUserSerializer,
    UserProfileSerializer,
)
from users.utils import get_user_roles


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return CreateUserSerializer

        return self.serializer_class

    def create(self, request, *args, **kwargs):
        create_user_serializer = CreateUserSerializer(data=request.data)

        if not create_user_serializer.is_valid():
            return Response("Bad request", status.HTTP_400_BAD_REQUEST)

        # TODO: check if email already exists
        # TODO: Assign user to a manager

        cleaned_data = create_user_serializer.data
        user = User(
            email=cleaned_data["email"],
            password=make_password(cleaned_data["password"]),
        )
        user.save()

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
