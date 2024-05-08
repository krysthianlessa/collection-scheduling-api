from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.contrib.auth.models import User
from core.models import Schedule, SharedCalendar

class MeSerializer(ModelSerializer):
    sector = SerializerMethodField(read_only=True)
    neighborhood = SerializerMethodField(read_only=True)
    full_name = SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "sector",
            "neighborhood",
            "full_name",
        ]

    def get_sector(self, user: User):
        shared_calendar = user.shared_calendar.filter(is_active=True).first()
        if shared_calendar:
            return shared_calendar.sector
        return ""

    def get_neighborhood(self, user: User):
        shared_calendar = user.shared_calendar.filter(is_active=True).first()
        if shared_calendar:
            return shared_calendar.neighborhood
        return ""

    def get_full_name(self, user: User):
        return user.get_full_name()


class ScheduleSerializer(ModelSerializer):
    whatsapp_message = SerializerMethodField(read_only=True)

    class Meta:
        model = Schedule
        exclude = [
            'created_by',
            'shared_calendar',
            'calendar_event_id',
            'has_sync'
        ]
        read_only_fields = ["whatsapp_message"]

    def get_whatsapp_message(self, schedule: Schedule):
        return schedule.whatsapp_message

    def create(self, validated_data):
        # Get the user making the request
        user = self.context['request'].user
        
        # Set the created_by field to the user
        validated_data['created_by'] = user
        
        # Query for an active SharedCalendar associated with the user
        shared_calendar = SharedCalendar.objects.filter(user=user, is_active=True).first()
        
        # If a valid SharedCalendar is found, set it as the shared_calendar field
        if shared_calendar:
            validated_data['shared_calendar'] = shared_calendar

        # Create the Schedule instance
        schedule = Schedule.objects.create(**validated_data)
        return schedule
