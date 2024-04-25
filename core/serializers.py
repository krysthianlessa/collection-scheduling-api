from rest_framework.serializers import ModelSerializer
from core.models import Schedule, SharedCalendar


class ScheduleSerializer(ModelSerializer):
    class Meta:
        model = Schedule
        fields = (
            "day",
            "start",
            "end",
            "full_name",
            "address",
            "phone",
        )

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
