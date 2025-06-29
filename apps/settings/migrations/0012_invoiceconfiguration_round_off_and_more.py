# Generated by Django 4.2.6 on 2023-10-28 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0011_invoiceconfiguration_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoiceconfiguration',
            name='round_off',
            field=models.BooleanField(default=False, verbose_name='Enable round-off'),
        ),
        migrations.AddField(
            model_name='invoiceconfiguration',
            name='show_qr_code',
            field=models.BooleanField(default=False, verbose_name='Show QR code on invoice'),
        ),
    ]
