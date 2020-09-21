from rest_framework import serializers

from cuser.models import CUser as User, Group, CUser

from users.utils import is_manager


class ManagedUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(source="user.id")
    email = serializers.EmailField(source="user.email", required=False)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)


class UserSerializer(serializers.ModelSerializer):
    managed_users = ManagedUserSerializer(source="manager", many=True)
    roles = GroupSerializer(source="groups", many=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "groups",
            "is_active",
            "is_staff",
            "is_superuser",
            "email",
            "date_joined",
            "last_login",
            "managed_users",
            "roles",
        ]


class CreateUserSerializer(serializers.Serializer):
    first_name = serializers.CharField(min_length=1, allow_null=False)
    last_name = serializers.CharField(min_length=1, allow_null=False)
    email = serializers.EmailField(min_length=1, allow_null=False)
    password = serializers.RegexField(
        r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", allow_null=False
    )


class UpdateUserSerializer(serializers.ModelSerializer):
    managed_users = ManagedUserSerializer(
        source="manager", many=True, required=False, allow_null=True
    )

    class Meta:
        model = User
        fields = ["is_active", "managed_users"]

    @staticmethod
    def validate_managed_users_are_not_managers_or_bosses(managed_users):
        managed_user_ids = [item["user"]["id"] for item in managed_users]
        managed_users = CUser.objects.filter(id__in=managed_user_ids).all()
        for user in managed_users:
            if user.is_superuser or is_manager(user):
                raise serializers.ValidationError(
                    "A manager can't manage other managers or bosses"
                )

    def validate(self, data):
        MANAGED_USERS = "manager"
        if MANAGED_USERS in data:
            self.validate_managed_users_are_not_managers_or_bosses(data[MANAGED_USERS])

        return data


class UserProfileSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=1, allow_null=False, required=True)
    is_superuser = serializers.BooleanField(allow_null=False, required=True)
    roles = serializers.ListField(allow_empty=True)
