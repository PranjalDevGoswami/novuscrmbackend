# Generated by Django 5.0.1 on 2024-02-06 12:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0017_project_estimated_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='estimated_time',
        ),
    ]
