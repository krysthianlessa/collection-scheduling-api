from django.db import models


class Schedule(models.Model):
    day = models.DateTimeField(blank=True, null=True)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    full_name = models.CharField(max_length=256)
    address =  models.CharField(max_length=256)
    phone = models.CharField(max_length=64)


class ScheduleWhatsAppIntegration(models.Model):
    schedule = models.ForeignKey("core.Schedule", on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)


class ScheduleCalendarIntegration(models.Model):
    schedule = models.ForeignKey("core.Schedule", on_delete=models.CASCADE)
    sync_at = models.DateTimeField(auto_now_add=True)
