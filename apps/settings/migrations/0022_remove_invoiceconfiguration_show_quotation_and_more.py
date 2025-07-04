# Generated by Django 4.2.6 on 2023-11-24 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0021_remove_invoiceconfiguration_show_finance_details'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoiceconfiguration',
            name='show_quotation',
        ),
        migrations.RemoveField(
            model_name='invoiceconfiguration',
            name='show_tax_invoice',
        ),
        migrations.RemoveField(
            model_name='invoiceconfiguration',
            name='status',
        ),
        migrations.AddField(
            model_name='invoiceconfiguration',
            name='tax_invoice_or_quotation',
            field=models.CharField(blank=True, choices=[('0', 'TAX INVOICE'), ('1', 'QUOTATION')], max_length=2, null=True),
        ),
    ]
