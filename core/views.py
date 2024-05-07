import multiprocessing
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from core.models import Schedule
from core.serializers import ScheduleSerializer
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_jwt.permissions import IsSuperUser
from core.services import CalendarService


class ScheduleViewSet(ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["has_sync"]
    permission_classes = [HasAPIKey | IsSuperUser]

    def perform_create(self, serializer: ScheduleSerializer):
        instance: Schedule = serializer.save()
        self._sync_to_google_calendar(instance)

    def perform_update(self, serializer: ScheduleSerializer):
        instance: Schedule = serializer.save()
        self._sync_to_google_calendar(instance)

    def _sync_to_google_calendar(self, instance: Schedule):
        process = multiprocessing.Process(
            target=CalendarService.sync_to_google_api,
            args=[instance],
        )
        process.start()
        return
