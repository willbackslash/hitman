from cuser.models import CUser
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from hitman.utils.viewset_mixin import PermissionByActionMixin
from hits.models import Hit, HitStatus
from hits.permissions import UserCanCreateHits, UserCanAssignHits
from hits.serializers import HitSerializer, CreateHitSerializer, UpdateHitSerializer
from users.models import ManagerUser
from users.utils import is_manager


class HitViewSet(PermissionByActionMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Hit.objects.all()
    serializer_class = HitSerializer
    permission_classes_by_action = {
        "create": [IsAuthenticated, UserCanCreateHits],
        "update": [IsAuthenticated, UserCanAssignHits],
    }
    http_method_names = ["get", "post", "put", "options"]

    def get_queryset(self):  # Filters the available hits by user role
        user = self.request.user

        if user.is_superuser:
            return self.queryset.all()

        if is_manager(user):
            return self.queryset.filter(
                Q(assigned_to=user)
                | Q(
                    assigned_to__in=[
                        lackey.user
                        for lackey in ManagerUser.objects.filter(manager=user).all()
                    ]
                )
            ).all()

        return self.queryset.filter(assigned_to=user).all()

    def get_serializer_class(self):
        if self.action == "create":
            return CreateHitSerializer
        if self.action == "update":
            return UpdateHitSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        create_hit_serializer = CreateHitSerializer(data=request.data)

        if not create_hit_serializer.is_valid():
            return Response(
                {"details": create_hit_serializer.errors}, status.HTTP_400_BAD_REQUEST
            )

        cleaned_data = create_hit_serializer.data
        hit = Hit(
            assigned_to=CUser.objects.get(email=cleaned_data["assigned_to"]),
            target_name=cleaned_data["target_name"],
            description=cleaned_data["description"],
            requester=request.user,
        )
        hit.save()

        return Response(self.serializer_class(hit).data, status.HTTP_201_CREATED)

    def update_status(self, hit_to_update, request, cleaned_data):
        if hit_to_update.assigned_to != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        try:
            if cleaned_data["status"] == HitStatus.COMPLETED:
                hit_to_update.mark_as_completed()

            if cleaned_data["status"] == HitStatus.FAILED:
                hit_to_update.mark_as_failed()
        except Exception as e:
            return Response({"detail": str(e)}, status.HTTP_403_FORBIDDEN)

        return Response(self.serializer_class(hit_to_update).data, status.HTTP_200_OK)

    def assign_hit(self, hit_to_update, cleaned_data):
        user_to_assign = CUser.objects.filter(
            email=cleaned_data["assigned_to"], is_active=True
        ).first()

        if not user_to_assign:
            return Response(
                {"detail": "the user doesn't exist or is not active"},
                status=status.HTTP_403_FORBIDDEN,
            )

        hit_to_update.assigned_to = user_to_assign
        hit_to_update.save()
        return Response(self.serializer_class(hit_to_update).data, status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        update_hit_serializer = UpdateHitSerializer(data=request.data, partial=True)

        if not update_hit_serializer.is_valid():
            return Response(update_hit_serializer.errors, status.HTTP_400_BAD_REQUEST)

        cleaned_data = update_hit_serializer.data
        hit_to_update = Hit.objects.get(pk=kwargs["pk"])

        if cleaned_data["status"] is not None:
            return self.update_status(hit_to_update, request, cleaned_data)

        if cleaned_data["assigned_to"] is not None:
            return self.assign_hit(hit_to_update, cleaned_data)

        return Response(status=status.HTTP_403_FORBIDDEN)
