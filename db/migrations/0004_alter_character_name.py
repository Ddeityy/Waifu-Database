# Generated by Django 4.1.5 on 2023-01-22 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0003_character'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='name',
            field=models.TextField(unique=True),
        ),
    ]
