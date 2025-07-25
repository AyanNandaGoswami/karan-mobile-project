# Generated by Django 4.2.6 on 2024-01-14 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0023_invoices_loan_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoices',
            name='invoice_total',
            field=models.FloatField(blank=True, null=True, verbose_name='Invoice total'),
        ),
        migrations.AddField(
            model_name='invoices',
            name='trash',
            field=models.BooleanField(default=False),
        ),
    ]
