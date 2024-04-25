from django.db.models.signals import pre_save
from django.dispatch import receiver
from core.models import SharedCalendar


@receiver(pre_save, sender=SharedCalendar)
def deactivate_shared_calendars(sender, instance: SharedCalendar, **kwargs):
    if instance.pk is None:
        SharedCalendar.objects.filter(
            user=instance.user,
        ).update(is_active=False)
