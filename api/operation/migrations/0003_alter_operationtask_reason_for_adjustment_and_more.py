# Generated by Django 4.2.10 on 2024-02-27 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0002_operationtask'),
    ]

    operations = [
        migrations.AlterField(
            model_name='operationtask',
            name='reason_for_adjustment',
            field=models.TextField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='operationtask',
            name='total_achievement',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]
