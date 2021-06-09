# Generated by Django 3.1.7 on 2021-06-06 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_auto_20210606_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='branch',
            field=models.CharField(choices=[('feruzi', 'feruzi'), ('fourways', 'fourways')], default='feruzi', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchase',
            name='branch',
            field=models.CharField(choices=[('feruzi', 'feruzi'), ('fourways', 'fourways')], default='fourways', max_length=254),
            preserve_default=False,
        ),
    ]
