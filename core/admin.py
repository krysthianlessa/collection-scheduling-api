from django.contrib import admin
from django.contrib.auth.models import Group, User
from core.models import Schedule, SharedCalendar


class SharedCalendarAdmin(admin.ModelAdmin):
    model = SharedCalendar


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
        return obj.calendar.sync_at is not None

    def whatsapp(self, obj) -> bool:
        return obj.whatsapp.sent_at is not None

admin.site.unregister(Group)

admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(SharedCalendar, SharedCalendarAdmin)
