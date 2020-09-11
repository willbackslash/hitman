from rest_framework import serializers

from cuser.models import CUser as User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]


class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=1, allow_null=False)
    password = serializers.CharField(min_length=4, allow_null=False)
