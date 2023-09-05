from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.table_block.blocks import TableBlock
# from blog.models import BlogPage
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.blocks import StreamBlock
from wagtailsurveyjs.models import AbstractSurveyJsFormPage


from wagtail.contrib.typed_table_block.blocks import TypedTableBlock
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import (
    RawHTMLBlock, BlockQuoteBlock,
    ChoiceBlock, StructBlock
    )

# from wagtail.blocks import (
#     RawHTMLBlock, BlockQuoteBlock,
#     ChoiceBlock, StructBlock
#     )
# new_table_options = {

#     'contextMenu': [
#         'row_above',
#         'row_below',
#         '---------',
#         'col_left',
#         'col_right',
#         '---------',
#         'remove_row',
#         'remove_col',
#         '---------',
#         'undo',
#         'redo',
#         '---------',
#         'copy',
#         'cut'
#         '---------',
#         'alignment',
#     ],
# }

# class DemoStreamBlock(blocks.StreamBlock):
#     title = blocks.CharBlock()
#     paragraph = blocks.RichTextBlock()
#     table = TypedTableBlock([
#             ('text', blocks.CharBlock()),
#             ('numeric', blocks.FloatBlock()),
#             ('rich_text', blocks.RichTextBlock()),
#             ('image', ImageChooserBlock()),
#             ('country', ChoiceBlock(choices=[
#                 ('be', 'Belgium'),
#                 ('fr', 'France'),
#                 ('de', 'Germany'),
#                 ('nl', 'Netherlands'),
#                 ('pl', 'Poland'),
#                 ('uk', 'United Kingdom'),
#             ])),
#         ])



class ServiceBlock(blocks.StructBlock):
    icon = blocks.RawHTMLBlock(required=True)
    icon_description = blocks.TextBlock()

class ServiceSectionBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    description = blocks.RichTextBlock()
    points = blocks.ListBlock(blocks.RichTextBlock(), required=False)

class HomePage(Page):
    # body = RichTextField(blank=True)
    body = StreamField([
        ('Topic', blocks.StructBlock([
            ('title', blocks.CharBlock()),
            ('subtitle', blocks.CharBlock()),
            ('description', blocks.RichTextBlock())])),

        ('Images', blocks.StructBlock([
            ('image_1', ImageChooserBlock()),
            ('image_2', ImageChooserBlock()),
            ('image_3', ImageChooserBlock())
        ])),

        ('WhatWeDo', blocks.StructBlock([
            ('heading', blocks.CharBlock()),
            ('subheading', blocks.CharBlock()),
            ('description1_title', blocks.CharBlock()),
            ('description1_text', blocks.RichTextBlock()),
            ('description1_link_text', blocks.CharBlock()),  # النص الذي سيظهر للمستخدم
            ('description1_link_url', blocks.URLBlock()),  # الرابط الذي سيربطه النص
            ('description2_title', blocks.CharBlock()),
            ('description2_text', blocks.RichTextBlock()),
             ('description2_link_text', blocks.CharBlock()),  # النص الذي سيظهر للمستخدم
            ('description2_link_url', blocks.URLBlock()),  # الرابط الذي سيربطه النص
        ])),
        ('RightCard', blocks.StructBlock([
            ('image', ImageChooserBlock()),
            ('title', blocks.CharBlock()),
            ('text', blocks.RichTextBlock()),
            ('link_text', blocks.CharBlock()),  # النص الذي سيظهر للمستخدم
            ('link_url', blocks.URLBlock())  # الرابط الذي سيربطه النص
        ])),
        ('LeftCard', blocks.StructBlock([
            ('image', ImageChooserBlock()),
            ('title', blocks.CharBlock()),
            ('text', blocks.RichTextBlock()),
            ('link_text', blocks.CharBlock()),  # النص الذي سيظهر للمستخدم
            ('link_url', blocks.URLBlock())
        ])),
        ('HeadingWithSubheading', blocks.StructBlock([
            ('heading', blocks.CharBlock()),
            ('subheading', blocks.CharBlock())
        ])),
        # ('service_list', ServiceListBlock(label="Service List")),
        ('service_list', ServiceBlock()),

        ('service_section', ServiceSectionBlock(label="Service Section")),
        ],use_json_field=True, blank=True, null=True)

    # tables = StreamField([
    #     ('tablesss', DemoStreamBlock(table_options=new_table_options))
    #     ],use_json_field=True, blank=True, null=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
        # FieldPanel('home_body'),
    ]

# class SurveyPage(AbstractSurveyJsFormPage):
#     parent_page_types = ['home.HomePage']

#     subpage_types = []
#     template = "home/survey_form_page.html"

#     content_panels = Page.content_panels