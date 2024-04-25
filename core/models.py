from django.db import models
from django.contrib.auth.models import User


class Schedule(models.Model):
    day = models.DateTimeField(blank=True, null=True)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    full_name = models.CharField(max_length=256)
    address =  models.CharField(max_length=256)
    phone = models.CharField(max_length=64)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    shared_calendar = models.ForeignKey(
        "core.SharedCalendar",
        on_delete=models.CASCADE,
        null=True,
        related_name="schedules",
    )


class ScheduleWhatsAppIntegration(models.Model):
    schedule = models.OneToOneField(
        "core.Schedule",
        related_name="whatsapp",
        on_delete=models.CASCADE,
    )
    sent_at = models.DateTimeField(auto_now_add=True)


class ScheduleCalendarIntegration(models.Model):
    schedule = models.OneToOneField(
        "core.Schedule",
        related_name="calendar",
        on_delete=models.CASCADE,
    )
    sync_at = models.DateTimeField(auto_now_add=True)


class SharedCalendar(models.Model):
    identify = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    sector = models.CharField(max_length=128)
    neighborhood = models.CharField(max_length=128)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shared_calendar",
    )

    def __str__(self) -> str:
        return f"{self.user.username} | {self.neighborhood} | {self.sector}"
