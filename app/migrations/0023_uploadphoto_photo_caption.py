# Generated by Django 3.2.1 on 2024-03-18 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_uploadphoto'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadphoto',
            name='photo_caption',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
