from django.contrib import admin
from django.contrib.auth.models import Group
from core.models import Schedule


class ScheduleAdmin(admin.ModelAdmin):
    model = Schedule

admin.site.unregister(Group)

admin.site.register(Schedule, ScheduleAdmin)
