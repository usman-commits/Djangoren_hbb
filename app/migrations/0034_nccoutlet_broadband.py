# Generated by Django 3.2.1 on 2024-03-21 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0033_auto_20240320_2229'),
    ]

    operations = [
        migrations.AddField(
            model_name='nccoutlet',
            name='broadband',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ncc_outlets', to='app.broadband'),
        ),
    ]
