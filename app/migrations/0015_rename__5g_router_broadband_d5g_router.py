# Generated by Django 5.0.1 on 2024-02-01 19:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_broadband_mifi_broadband_odu_broadband_router_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='broadband',
            old_name='_5G_Router',
            new_name='d5G_Router',
        ),
    ]
