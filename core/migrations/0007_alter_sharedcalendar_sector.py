# Generated by Django 5.0.4 on 2024-04-25 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_sharedcalendar_is_active_sharedcalendar_sector'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sharedcalendar',
            name='sector',
            field=models.CharField(max_length=128),
        ),
    ]
