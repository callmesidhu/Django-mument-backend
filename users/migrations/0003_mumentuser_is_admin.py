# Generated by Django 5.2.1 on 2025-06-14 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_mumentuser_players_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='mumentuser',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
