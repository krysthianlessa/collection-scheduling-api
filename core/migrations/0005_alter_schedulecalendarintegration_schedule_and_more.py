# Generated by Django 5.0.4 on 2024-04-24 17:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_schedulecalendarintegration_schedule_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedulecalendarintegration',
            name='schedule',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='calendar', to='core.schedule'),
        ),
        migrations.AlterField(
            model_name='schedulewhatsappintegration',
            name='schedule',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='whatsapp', to='core.schedule'),
        ),
        migrations.CreateModel(
            name='SharedCalendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identify', models.CharField(max_length=128)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
