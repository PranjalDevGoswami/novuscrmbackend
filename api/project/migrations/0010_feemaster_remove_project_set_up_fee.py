# Generated by Django 5.0.1 on 2024-02-05 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_alter_client_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeeMaster',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fee', models.DecimalField(decimal_places=2, max_digits=8)),
                ('is_default', models.BooleanField(default=True)),
                ('description', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='project',
            name='set_up_fee',
        ),
    ]
