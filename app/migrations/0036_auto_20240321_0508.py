# Generated by Django 3.2.1 on 2024-03-21 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0035_auto_20240320_2342'),
    ]

    operations = [
        migrations.AddField(
            model_name='reactivationreport',
            name='Region',
            field=models.CharField(choices=[('North East', 'North East'), ('North West', 'North West'), ('South East', 'South East'), ('South South', 'South South'), ('Lagos', 'Lagos'), ('West', 'West')], default='North East', max_length=100),
        ),
        migrations.AddField(
            model_name='reactivationreport',
            name='State',
            field=models.CharField(default='kano', max_length=100),
        ),
    ]
