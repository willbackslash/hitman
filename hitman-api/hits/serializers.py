from rest_framework import serializers

from hits.models import HitStatus, Hit
from users.serializers import UserSerializer


class HitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hit
        fields = [
            "id",
            "target_name",
            "description",
            "status",
            "assigned_to",
            "requester",
            "created_at",
            "updated_at",
        ]

    assigned_to = UserSerializer()
    requester = UserSerializer()


class CreateHitSerializer(serializers.Serializer):
    assigned_to = serializers.EmailField(
        required=True, allow_blank=False, allow_null=False
    )
    target_name = serializers.CharField(
        min_length=1, max_length=255, required=True, allow_null=False, allow_blank=False
    )
    description = serializers.CharField(
        min_length=1, max_length=255, required=True, allow_null=False, allow_blank=False
    )


class UpdateHitSerializer(serializers.Serializer):
    assigned_to = serializers.EmailField(required=True, allow_null=True)
    status = serializers.ChoiceField(
        choices=HitStatus.choices, required=True, allow_null=True
    )
