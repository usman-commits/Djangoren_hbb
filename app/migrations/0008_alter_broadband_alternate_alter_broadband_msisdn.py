# Generated by Django 5.0.1 on 2024-01-20 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_broadband_alternate_alter_broadband_msisdn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='broadband',
            name='Alternate',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='broadband',
            name='MSISDN',
            field=models.IntegerField(),
        ),
    ]
