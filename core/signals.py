import multiprocessing
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from core.models import Schedule, SharedCalendar
from core.services import CalendarService
import logging

logger = logging.getLogger('default')


@receiver(pre_save, sender=SharedCalendar)
def deactivate_shared_calendars(sender, instance: SharedCalendar, **kwargs):
    if instance.pk is None:
        SharedCalendar.objects.filter(
            user=instance.user,
        ).update(is_active=False)

@receiver(post_save, sender=Schedule)
def sync_google_calendar(sender, instance: Schedule, **kwargs):
    process = multiprocessing.Process(
        target=CalendarService.sync_to_google_api,
        args=[instance],
    )
    process.start()
    # try:
    #     CalendarService.sync_to_google_api(instance)
    # except Exception as error:
    #     logger.warning("Error when try sync with google calendar %s", error, exec_info=1)