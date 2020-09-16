from rest_framework import serializers

from hits.models import HitStatus
from users.serializers import UserSerializer


class HitSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    assigned_to = UserSerializer()
    target_name = serializers.CharField(
        min_length=1, max_length=255, required=True, allow_null=False, allow_blank=False
    )
    description = serializers.CharField(
        min_length=1, max_length=255, required=True, allow_null=False, allow_blank=False
    )
    status = serializers.ChoiceField(
        choices=HitStatus.choices, required=True, allow_null=False, allow_blank=False
    )
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
