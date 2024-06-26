# Generated by Django 5.0.4 on 2024-04-22 02:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateTimeField(blank=True, null=True)),
                ('start', models.DateTimeField(blank=True, null=True)),
                ('end', models.DateTimeField(blank=True, null=True)),
                ('full_name', models.CharField(max_length=256)),
                ('address', models.CharField(max_length=256)),
                ('phone', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleCalendarIntegration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sync_at', models.DateTimeField(auto_now_add=True)),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.schedule')),
            ],
        ),
        migrations.CreateModel(
            name='ScheduleWhatsAppIntegration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.schedule')),
            ],
        ),
    ]
