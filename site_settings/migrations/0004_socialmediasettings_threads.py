# Generated by Django 4.2.3 on 2023-07-27 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_settings', '0003_socialmediasettings_instagram_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialmediasettings',
            name='threads',
            field=models.URLField(blank=True, help_text='threads URL', null=True),
        ),
    ]