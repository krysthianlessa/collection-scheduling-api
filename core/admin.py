from django.contrib import admin
from django.contrib.auth.models import Group
from core.models import Schedule, SharedCalendar, ScheduleWhatsAppIntegration, ScheduleCalendarIntegration


class SharedCalendarAdmin(admin.ModelAdmin):
    model = SharedCalendar

class ScheduleWhatsAppIntegrationAdmin(admin.ModelAdmin):
    model = ScheduleWhatsAppIntegration

class ScheduleCalendarIntegrationAdmin(admin.ModelAdmin):
    model = ScheduleCalendarIntegration


class ScheduleAdmin(admin.ModelAdmin):
    model = Schedule
    add_fieldsets = []
    readonly_fields = (
        "day",
        "start",
        "end",
        "full_name",
        "address",
        "phone",
        "created_by",
    )
    list_display = (
        "day",
        "start",
        "end",
        "full_name",
        "created_by",
        "calendar",
        "whatsapp",
    )

    def calendar(self, obj) -> bool:
        calendar = obj.calendar_integration.order_by("id").last()
        return calendar and calendar.sync_at is not None

    def whatsapp(self, obj) -> bool:
        whatsapp = obj.whatsapp_integration.order_by("id").last()
        return whatsapp and whatsapp.sent_at is not None

    def has_add_permission(self, request, obj=None):
        return False

admin.site.unregister(Group)

admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(ScheduleWhatsAppIntegration, ScheduleWhatsAppIntegrationAdmin)
admin.site.register(ScheduleCalendarIntegration, ScheduleCalendarIntegrationAdmin)
admin.site.register(SharedCalendar, SharedCalendarAdmin)
