from rest_framework.serializers import ModelSerializer
from core.models import Schedule


class ScheduleSerializer(ModelSerializer):
    class Meta:
        model = Schedule
