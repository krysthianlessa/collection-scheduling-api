# Generated by Django 5.0.4 on 2024-05-09 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_alter_schedulecalendarintegration_schedule_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='has_sync',
            field=models.BooleanField(default=False, verbose_name='This info was synced with WhatsApp'),
        ),
    ]
