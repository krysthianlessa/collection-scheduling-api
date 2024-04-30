# Generated by Django 5.0.4 on 2024-04-30 23:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_sharedcalendar_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='calendar_event_id',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='day_of_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='schedule',
            name='has_sync',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='day',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='ScheduleHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sync_at', models.DateTimeField()),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='core.schedule')),
            ],
        ),
    ]
