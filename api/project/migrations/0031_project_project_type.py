# Generated by Django 4.2.10 on 2024-02-23 06:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0030_projecttype'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project.projecttype'),
        ),
    ]