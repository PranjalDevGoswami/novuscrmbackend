# Generated by Django 4.2.10 on 2024-03-07 12:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0037_salesowner_remove_project_currency_symbol_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='man_days',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='remaining_interview',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='remaining_time',
            field=models.DurationField(blank=True, default=datetime.timedelta(0), null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='total_achievement',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]
