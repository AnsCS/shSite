# Generated by Django 4.2.3 on 2023-07-27 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socialmediasettings',
            name='site',
        ),
    ]
