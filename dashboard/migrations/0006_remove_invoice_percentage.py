# Generated by Django 2.2.12 on 2021-09-15 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_invoice_percentage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='percentage',
        ),
    ]
