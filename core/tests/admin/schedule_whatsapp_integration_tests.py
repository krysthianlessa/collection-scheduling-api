from django.test import TestCase, RequestFactory
from django.contrib.admin.sites import AdminSite
from core.models import ScheduleWhatsAppIntegration
from core.admin import ScheduleWhatsAppIntegrationAdmin


class ScheduleWhatsAppIntegrationAdminTestCase(TestCase):
    def setUp(self):
        self.integration = ScheduleWhatsAppIntegration.objects.create()
        self.factory = RequestFactory()

    def test_str_method(self):
        integration_admin = ScheduleWhatsAppIntegrationAdmin(model=ScheduleWhatsAppIntegration, admin_site=AdminSite())
        expected_output = f"{self.integration.id} - [schedule: None]: "
        self.assertEqual(str(self.integration), expected_output)

    def test_display_methods(self):
        integration_admin = ScheduleWhatsAppIntegrationAdmin(model=ScheduleWhatsAppIntegration, admin_site=AdminSite())
        request = self.factory.get("/admin/core/schedulewhatsappintegration/")
        rendered_fieldsets = integration_admin.get_fieldsets(request)
        self.assertEqual(rendered_fieldsets[0][1]["fields"], ("schedule", "sent_at"))
        list_display = integration_admin.get_list_display(None)
        self.assertEqual(list_display, ("id", "schedule", "sent_at"))

    def test_has_add_permission(self):
        integration_admin = ScheduleWhatsAppIntegrationAdmin(model=ScheduleWhatsAppIntegration, admin_site=AdminSite())
        request = self.factory.get("/admin/core/schedulewhatsappintegration/add/")
        self.assertFalse(integration_admin.has_add_permission(request))

    def test_has_delete_permission(self):
        integration_admin = ScheduleWhatsAppIntegrationAdmin(model=ScheduleWhatsAppIntegration, admin_site=AdminSite())
        request = self.factory.get("/admin/core/schedulewhatsappintegration/")
        self.assertFalse(integration_admin.has_delete_permission(request, self.integration))

    def test_has_change_permission(self):
        integration_admin = ScheduleWhatsAppIntegrationAdmin(model=ScheduleWhatsAppIntegration, admin_site=AdminSite())
        request = self.factory.get("/admin/core/schedulewhatsappintegration/")
        self.assertTrue(integration_admin.has_change_permission(request, self.integration))
