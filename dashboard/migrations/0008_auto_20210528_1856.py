# Generated by Django 3.1.7 on 2021-05-28 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20210526_0902'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payroll',
            name='id',
        ),
        migrations.AddField(
            model_name='payroll',
            name='invoice_no',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]