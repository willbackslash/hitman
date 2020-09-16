from cuser.models import CUser
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from hits.models import Hit
from hits.permissions import UserCanCreateHits
from hits.serializers import HitSerializer, CreateHitSerializer
from users.models import ManagerUser
from users.utils import get_user_roles


class HitViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Hit.objects.all()
    serializer_class = HitSerializer
    permission_classes_by_action = {"create": [IsAuthenticated, UserCanCreateHits]}

    def get_queryset(self):  # Filters the available hits by user role
        user = self.request.user
        roles = get_user_roles(user)

        if user.is_superuser:
            return self.queryset

        if "manager" in roles:
            return self.queryset.filter(
                Q(assigned_to=user)
                | Q(
                    assigned_to__in=[
                        lackey.user
                        for lackey in ManagerUser.objects.filter(manager=user).all()
                    ]
                )
            )

        return self.queryset.filter(assigned_to=user)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateHitSerializer

        return self.serializer_class

    def create(self, request, *args, **kwargs):
        create_hit_serializer = CreateHitSerializer(data=request.data)

        if not create_hit_serializer.is_valid():
            return Response("Bad request", status.HTTP_400_BAD_REQUEST)

        cleaned_data = create_hit_serializer.data
        hit = Hit(
            assigned_to=CUser.objects.get(email=cleaned_data["assigned_to"]),
            target_name=cleaned_data["target_name"],
            description=cleaned_data["description"],
            requester=request.user,
        )
        hit.save()

        return Response(self.serializer_class(hit).data, status.HTTP_201_CREATED)
