# Generated by Django 3.2.1 on 2024-03-20 14:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_auto_20240320_0721'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadphoto',
            name='Region',
        ),
        migrations.RemoveField(
            model_name='uploadphoto',
            name='State',
        ),
    ]
