# Generated by Django 5.0.1 on 2024-02-07 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_rename__5g_router_broadband_d5g_router'),
    ]

    operations = [
        migrations.RenameField(
            model_name='broadband',
            old_name='name',
            new_name='HSE_name',
        ),
        migrations.AddField(
            model_name='broadband',
            name='Customer_name',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
