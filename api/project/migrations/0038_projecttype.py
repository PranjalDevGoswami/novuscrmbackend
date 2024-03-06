# Generated by Django 4.2.10 on 2024-03-06 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0037_salesowner_remove_project_currency_symbol_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='projectType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
