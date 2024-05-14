from django.test import TestCase, RequestFactory
from django.contrib.admin.sites import AdminSite
from django.contrib.auth.models import User
from core.models import SharedCalendar
from core.admin import SharedCalendarAdmin


class SharedCalendarAdminTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.shared_calendar = SharedCalendar.objects.create(
            identify="123456", is_active=True, sector="Sector A", neighborhood="Neighborhood X", user=self.user
        )
        self.factory = RequestFactory()

    def test_str_method(self):
        shared_calendar_admin = SharedCalendarAdmin(model=SharedCalendar, admin_site=AdminSite())
        expected_output = f"{self.user.username} | {self.shared_calendar.neighborhood} | {self.shared_calendar.sector}"
        self.assertEqual(str(self.shared_calendar), expected_output)

    def test_display_methods(self):
        shared_calendar_admin = SharedCalendarAdmin(model=SharedCalendar, admin_site=AdminSite())
        request = self.factory.get("/admin/core/sharedcalendar/")
        rendered_fieldsets = shared_calendar_admin.get_fieldsets(request)
        self.assertEqual(
            rendered_fieldsets[0][1]["fields"], ("identify", "is_active", "sector", "neighborhood", "user")
        )
        list_display = shared_calendar_admin.get_list_display(None)
        self.assertEqual(list_display, ("identify", "is_active", "sector", "neighborhood", "user"))

    def test_has_add_permission(self):
        shared_calendar_admin = SharedCalendarAdmin(model=SharedCalendar, admin_site=AdminSite())
        request = self.factory.get("/admin/core/sharedcalendar/add/")
        self.assertTrue(shared_calendar_admin.has_add_permission(request))

    def test_has_delete_permission(self):
        shared_calendar_admin = SharedCalendarAdmin(model=SharedCalendar, admin_site=AdminSite())
        request = self.factory.get("/admin/core/sharedcalendar/")
        self.assertTrue(shared_calendar_admin.has_delete_permission(request, self.shared_calendar))

    def test_has_change_permission(self):
        shared_calendar_admin = SharedCalendarAdmin(model=SharedCalendar, admin_site=AdminSite())
        request = self.factory.get("/admin/core/sharedcalendar/")
        self.assertTrue(shared_calendar_admin.has_change_permission(request, self.shared_calendar))

    def test_signal_deactivates_other_shared_calendars(self):
        other_shared_calendar = SharedCalendar.objects.create(
            identify="789012", is_active=True, sector="Sector B", neighborhood="Neighborhood Y", user=self.user
        )
        self.assertTrue(other_shared_calendar.is_active)

        # Saving a new shared calendar should deactivate the other one
        new_shared_calendar = SharedCalendar.objects.create(
            identify="345678", is_active=True, sector="Sector C", neighborhood="Neighborhood Z", user=self.user
        )

        # Refresh the other_shared_calendar instance from the database
        other_shared_calendar.refresh_from_db()
        self.assertFalse(other_shared_calendar.is_active)
