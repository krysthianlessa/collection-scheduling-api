from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from core.models import Schedule, ScheduleWhatsAppIntegration, ScheduleCalendarIntegration
from core.admin import ScheduleAdmin


class ScheduleAdminTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.schedule = Schedule.objects.create(
            day="2024-05-14", start="08:00", end="08:00", full_name="John Doe", created_by=self.user
        )
        self.factory = RequestFactory()

    def test_readonly_fields(self):
        admin_instance = ScheduleAdmin(model=Schedule, admin_site=AdminSite())
        self.assertEqual(
            admin_instance.get_readonly_fields(None),
            ["day", "start", "end", "full_name", "address", "phone", "created_by"],
        )

    def test_has_add_permission(self):
        admin_instance = ScheduleAdmin(model=Schedule, admin_site=AdminSite())
        request = self.factory.get("/admin/core/schedule/add/")
        request.user = self.user
        self.assertFalse(admin_instance.has_add_permission(request))

    def test_calendar_display(self):
        admin_instance = ScheduleAdmin(model=Schedule, admin_site=AdminSite())
        ScheduleCalendarIntegration.objects.create(schedule=self.schedule, sync_at="2024-05-14 10:00")
        self.assertTrue(admin_instance.calendar(self.schedule))

    def test_whatsapp_display(self):
        admin_instance = ScheduleAdmin(model=Schedule, admin_site=AdminSite())
        ScheduleWhatsAppIntegration.objects.create(schedule=self.schedule, sent_at="2024-05-14 10:00")
        self.assertTrue(admin_instance.whatsapp(self.schedule))
