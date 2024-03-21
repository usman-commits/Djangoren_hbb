# Generated by Django 3.2.1 on 2024-03-21 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_auto_20240320_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nccoutlet',
            name='Region',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='nccoutlet',
            name='State',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='reactivationreport',
            name='Region',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='reactivationreport',
            name='State',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='uploadphoto',
            name='Region',
            field=models.CharField(choices=[('North East', 'North East'), ('North West', 'North West'), ('South East', 'South East'), ('South South', 'South South'), ('Lagos', 'Lagos'), ('West', 'West')], default='North East', max_length=100),
        ),
        migrations.AlterField(
            model_name='uploadphoto',
            name='State',
            field=models.CharField(blank=True, choices=[], max_length=100),
        ),
    ]