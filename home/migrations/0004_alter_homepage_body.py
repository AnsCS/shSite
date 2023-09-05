# Generated by Django 4.2.4 on 2023-09-04 21:56

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_homepage_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='body',
            field=wagtail.fields.StreamField([('Topic', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('subtitle', wagtail.blocks.CharBlock()), ('description', wagtail.blocks.RichTextBlock())])), ('Images', wagtail.blocks.StructBlock([('image_1', wagtail.images.blocks.ImageChooserBlock()), ('image_2', wagtail.images.blocks.ImageChooserBlock()), ('image_3', wagtail.images.blocks.ImageChooserBlock())])), ('WhatWeDo', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock()), ('subheading', wagtail.blocks.CharBlock()), ('description1_title', wagtail.blocks.CharBlock()), ('description1_text', wagtail.blocks.RichTextBlock()), ('description1_link_text', wagtail.blocks.CharBlock()), ('description1_link_url', wagtail.blocks.URLBlock()), ('description2_title', wagtail.blocks.CharBlock()), ('description2_text', wagtail.blocks.RichTextBlock()), ('description2_link_text', wagtail.blocks.CharBlock()), ('description2_link_url', wagtail.blocks.URLBlock())])), ('RightCard', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('title', wagtail.blocks.CharBlock()), ('text', wagtail.blocks.RichTextBlock()), ('link_text', wagtail.blocks.CharBlock()), ('link_url', wagtail.blocks.URLBlock())])), ('LeftCard', wagtail.blocks.StructBlock([('image', wagtail.images.blocks.ImageChooserBlock()), ('title', wagtail.blocks.CharBlock()), ('text', wagtail.blocks.RichTextBlock()), ('link_text', wagtail.blocks.CharBlock()), ('link_url', wagtail.blocks.URLBlock())])), ('HeadingWithSubheading', wagtail.blocks.StructBlock([('heading', wagtail.blocks.CharBlock()), ('subheading', wagtail.blocks.CharBlock())])), ('service_list', wagtail.blocks.StructBlock([('icon', wagtail.blocks.RawHTMLBlock(required=True)), ('icon_description', wagtail.blocks.TextBlock())])), ('service_section', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('description', wagtail.blocks.RichTextBlock()), ('points', wagtail.blocks.ListBlock(wagtail.blocks.RichTextBlock(), required=False))], label='Service Section'))], null=True, use_json_field=True),
        ),
    ]
