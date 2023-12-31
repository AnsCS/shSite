# Generated by Django 4.2.4 on 2023-08-30 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
        ('blog', '0002_remove_blogpage_featured_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blogpage',
            name='featured_images',
        ),
        migrations.AddField(
            model_name='blogpage',
            name='featured_image',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image'),
        ),
    ]
