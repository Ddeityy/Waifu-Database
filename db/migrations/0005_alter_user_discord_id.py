# Generated by Django 4.1.5 on 2023-01-22 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0004_alter_character_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='discord_id',
            field=models.IntegerField(unique=True),
        ),
    ]