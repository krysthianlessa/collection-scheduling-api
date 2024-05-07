from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from core.models import Schedule
from core.serializers import ScheduleSerializer
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_jwt.permissions import IsSuperUser


class ScheduleViewSet(ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["has_sync"]
    permission_classes = [HasAPIKey | IsSuperUser]
