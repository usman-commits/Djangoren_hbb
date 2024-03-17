# Generated by Django 5.0.1 on 2024-01-27 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_broadband_alternate_alter_broadband_msisdn'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(max_length=50)),
                ('devices_sold', models.IntegerField(default=0)),
                ('date', models.DateField()),
                ('device_type', models.CharField(max_length=50)),
            ],
        ),
    ]
