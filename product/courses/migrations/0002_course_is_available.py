# Generated by Django 4.2.10 on 2024-08-19 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_available',
            field=models.BooleanField(default=False, verbose_name='Доступность курса'),
        ),
    ]
