# Generated by Django 4.2.10 on 2024-02-27 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0004_operationteam_daily_work_time_operationteam_date_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OperationTask',
        ),
    ]
