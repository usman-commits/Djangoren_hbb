# Generated by Django 5.0.1 on 2024-02-10 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_rename_name_nccoutlet_hse_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchivedData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('value', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MainData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('value', models.CharField(max_length=100)),
            ],
        ),
    ]
