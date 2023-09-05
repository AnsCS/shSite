# Generated by Django 4.2.4 on 2023-09-01 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_alter_sitesettings_text_alignment'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='button_style',
            field=models.CharField(choices=[('btn-primary', 'Primary'), ('btn-secondary', 'Secondary'), ('btn-success', 'Success')], default='btn-primary', max_length=255),
        ),
    ]
