import multiprocessing
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from core.models import SharedCalendar, ScheduleWhatsAppIntegration, ScheduleCalendarIntegration
from core.services import CalendarService


@receiver(pre_save, sender=SharedCalendar)
def deactivate_shared_calendars(sender, instance: SharedCalendar, **kwargs):
    if instance.pk is None:
        SharedCalendar.objects.filter(
            user=instance.user,
        ).update(is_active=False)

@receiver(post_save, sender=ScheduleCalendarIntegration)
def sync_google_calendar(sender, instance: ScheduleCalendarIntegration, **kwargs):
    process = multiprocessing.Process(
        target=CalendarService.sync_to_google_api,
        args=(123, 'abc')
    )
    process.start()
