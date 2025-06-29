# Generated by Django 4.2.6 on 2023-10-26 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0009_alter_invoicepdftemplate_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='UniqueIdConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created timestamp')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Last updated at')),
                ('type', models.CharField(choices=[('customer', 'Customer'), ('invoice', 'Invoice')], default='customer', max_length=10)),
                ('prefix', models.CharField(blank=True, max_length=5, null=True, verbose_name='Prefix for Customer-Id')),
                ('id_length', models.IntegerField(verbose_name='Length of Customer-Id')),
                ('postfix', models.CharField(blank=True, max_length=5, null=True, verbose_name='Postfix for Customer-Id')),
                ('start_id', models.IntegerField(default=0, verbose_name='Start indexing id')),
                ('counter', models.IntegerField(default=0)),
                ('status', models.IntegerField(choices=[(1, 'Active'), (0, 'In-active')], default=1)),
            ],
            options={
                'verbose_name': 'Unique-ID configuration',
                'verbose_name_plural': 'Unique-ID configurations',
            },
        ),
        migrations.DeleteModel(
            name='CustomerUniqueIdConfig',
        ),
    ]
