# Generated by Django 5.0.4 on 2024-04-25 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_schedule_shared_calendar'),
    ]

    operations = [
        migrations.AddField(
            model_name='sharedcalendar',
            name='neighborhood',
            field=models.CharField(max_length=128, null=True),
        ),
    ]