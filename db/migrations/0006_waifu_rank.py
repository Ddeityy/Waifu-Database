# Generated by Django 4.1.5 on 2023-01-25 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0005_alter_user_discord_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='waifu',
            name='rank',
            field=models.TextField(null=True),
        ),
    ]