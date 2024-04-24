from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import generics, mixins
from core.models import Schedule
from core.serializers import ScheduleSerializer


class ScheduleViewSet(ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
