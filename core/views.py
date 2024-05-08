from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from core.models import Schedule
from core.serializers import ScheduleSerializer, MeSerializer
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.permissions import IsAuthenticated


class ScheduleViewSet(ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["has_sync"]
    permission_classes = [HasAPIKey | IsAuthenticated]

    @action(detail=False, methods=["post"], url_path="(?P<schedule_id>\\d+)/whatsapp")
    def whatsapp_synced(self, request, schedule_id, *args, **kwargs):
        Schedule.objects.filter(id=schedule_id).update(has_sync=True)

        return Response(status=status.HTTP_200_OK)

class MeView(APIView):
    serializer_class = MeSerializer

    def get(self, request, *args, **kwargs):
        serializer = MeSerializer(request.user)
        return Response(serializer.data)
