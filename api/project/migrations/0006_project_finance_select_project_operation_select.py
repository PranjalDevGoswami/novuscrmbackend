# Generated by Django 5.0.1 on 2024-01-29 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0005_project_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='finance_select',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='project',
            name='operation_select',
            field=models.BooleanField(default=False),
        ),
    ]