from cuser.models import CUser as User
from rest_framework import viewsets, status
from rest_framework.response import Response

from users.serializers import UserSerializer, CreateUserSerializer


class UserViewSet(viewsets.ModelViewSet):
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
            password=cleaned_data["password"],
        )
        user.save()

        return Response(self.serializer_class(user).data, status.HTTP_201_CREATED)
