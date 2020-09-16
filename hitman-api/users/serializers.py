from rest_framework import serializers

from cuser.models import CUser as User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email"]


class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=1, allow_null=False)
    password = serializers.RegexField(
        r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", allow_null=False
    )


class UserProfileSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=1, allow_null=False, required=True)
    is_super_user = serializers.BooleanField(allow_null=False, required=True)
    roles = serializers.ListField(allow_empty=True)
