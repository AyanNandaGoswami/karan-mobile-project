# Generated by Django 4.2.6 on 2024-01-04 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0022_invoices_advance_emi_invoices_margin_money'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoices',
            name='loan_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
