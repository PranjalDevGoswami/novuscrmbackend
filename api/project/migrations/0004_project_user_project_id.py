# Generated by Django 5.0.1 on 2024-01-29 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_remove_project_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='user_project_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]