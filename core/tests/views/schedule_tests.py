from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from core.models import Schedule, ScheduleWhatsAppIntegration
from core.views import ScheduleViewSet


class ScheduleViewSetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.schedule = Schedule.objects.create(
            day_of_birth="2000-01-01",
            day="2024-05-14",
            start="08:00",
            end="17:00",
            full_name="John Doe",
            address="123 Main St",
            phone="555-1234",
            created_by=self.user,
        )
        self.factory = APIRequestFactory()

    def test_whatsapp_synced_action(self):
        view = ScheduleViewSet.as_view({"post": "whatsapp_synced"})
        request = self.factory.post("/schedule/whatsapp", {"schedule_id": self.schedule.id})
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.schedule.refresh_from_db()
        self.assertTrue(self.schedule.has_sync)
        integration = ScheduleWhatsAppIntegration.objects.get(schedule=self.schedule)
        self.assertIsNotNone(integration)

    def test_post_save_signal(self):
        self.schedule.refresh_from_db()
        self.assertFalse(self.schedule.has_sync)
        Schedule.objects.filter(id=self.schedule.id).update(has_sync=True)
        self.schedule.refresh_from_db()
        self.assertTrue(self.schedule.has_sync)
