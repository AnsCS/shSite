# Generated by Django 4.2.4 on 2023-08-30 14:43

import blog.models
from django.db import migrations, models
import django.db.models.deletion
import django_ckeditor_5.fields
import modelcluster.contrib.taggit
import modelcluster.fields
import wagtail.blocks
import wagtail.contrib.forms.models
import wagtail.contrib.table_block.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtailmetadata.models
import wagtailtables.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0005_auto_20220424_2025'),
        ('wagtailcore', '0083_workflowcontenttype'),
        ('wagtailimagecaptions', '0002_rename_extendedrendition_captionedrendition'),
        ('wagtailimages', '0025_alter_image_file_alter_rendition_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('icon', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
            ],
            options={
                'verbose_name_plural': 'blog categories',
            },
        ),
        migrations.CreateModel(
            name='BlogIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('intro', wagtail.fields.RichTextField()),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='BlogPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('date', models.DateField()),
                ('intro', models.CharField(max_length=250)),
                ('body', django_ckeditor_5.fields.CKEditor5Field()),
                ('summary', wagtail.fields.RichTextField()),
                ('view_count', models.PositiveIntegerField(default=0)),
                ('show_body', wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock()), ('paragraph', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock()), ('video', wagtail.blocks.StructBlock([('url', wagtail.blocks.URLBlock()), ('max_width', wagtail.blocks.IntegerBlock(default=1094, max_value=1400, min_value=100)), ('max_height', wagtail.blocks.IntegerBlock(default=529, max_value=1000, min_value=100)), ('title', wagtail.blocks.CharBlock(required=False))])), ('aligned_text', wagtail.blocks.StructBlock([('text', wagtail.blocks.RichTextBlock()), ('alignment', wagtail.blocks.ChoiceBlock(choices=[('left', 'Left'), ('center', 'Center'), ('right', 'Right')]))])), ('code', wagtail.blocks.StructBlock([('code', wagtail.blocks.TextBlock()), ('language', wagtail.blocks.CharBlock(help_text='Programming language (e.g. python, javascript)', required=False))])), ('raw_html', wagtail.blocks.RawHTMLBlock()), ('blockquote', wagtail.blocks.StructBlock([('text', wagtail.blocks.TextBlock(required=True)), ('name', wagtail.blocks.CharBlock(required=False))])), ('table', wagtail.blocks.StreamBlock([('table', wagtail.contrib.table_block.blocks.TableBlock(table_options={'contextMenu': ['row_above', 'row_below', '---------', 'col_left', 'col_right', '---------', 'remove_row', 'remove_col', '---------', 'undo', 'redo', '---------', 'copy', 'cut---------', 'alignment']}))])), ('tables', wagtail.blocks.StreamBlock([('table_block', wagtail.blocks.StructBlock([('table_data', wagtail.blocks.TextBlock(default='[]')), ('caption', wagtail.blocks.CharBlock(required=False)), ('header_row', wagtail.blocks.BooleanBlock(required=False)), ('header_col', wagtail.blocks.BooleanBlock(required=False)), ('table_type', wagtail.blocks.ChoiceBlock(choices=wagtailtables.blocks.get_choices))], toolbar=[{'content': 'format_align_left', 'k': 'text-align', 'type': 'i', 'v': 'left'}, {'content': 'format_align_center', 'k': 'text-align', 'type': 'i', 'v': 'center'}, {'content': 'format_align_right', 'k': 'text-align', 'type': 'i', 'v': 'right'}, {'content': 'format_bold', 'k': 'font-weight', 'type': 'i', 'v': '600'}, {'content': 'format_italic', 'k': 'font-style', 'type': 'i', 'v': 'italic'}, {'content': 'border_left', 'k': 'border-left', 'type': 'i', 'v': '1px solid'}, {'content': 'border_right', 'k': 'border-right', 'type': 'i', 'v': '1px solid'}, {'content': 'border_top', 'k': 'border-top', 'type': 'i', 'v': '1px solid'}, {'content': 'format_size', 'k': 'font-size', 'type': 'i', 'v': '16px'}]))])), ('person', wagtail.blocks.StructBlock([('name', wagtail.blocks.CharBlock()), ('fullName_color', wagtail.blocks.TextBlock(help_text='Hexadecimal, rgba, or CSS color notation (e.g. #ff0011)', required=False)), ('pe_image', wagtail.images.blocks.ImageChooserBlock()), ('biography', wagtail.blocks.RichTextBlock()), ('text_color', wagtail.blocks.TextBlock(help_text='Hexadecimal, rgba, or CSS color notation (e.g. #ff0011)', required=False)), ('background_color', wagtail.blocks.TextBlock(help_text='Hexadecimal, rgba, or CSS color notation (e.g. #ff0011)', required=False)), ('description', wagtail.blocks.StreamBlock([('description_item', wagtail.blocks.RichTextBlock(required=False))], required=False))], icon='user')), ('recipe', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('ingredients', wagtail.blocks.ListBlock(blog.models.IngredientBlock)), ('instructions', wagtail.blocks.RichTextBlock())])), ('note', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock()), ('description', wagtail.blocks.RichTextBlock())]))], null=True, use_json_field=True)),
                ('categories', modelcluster.fields.ParentalManyToManyField(to='blog.blogcategory')),
                ('featured_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimages.image')),
                ('search_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailimagecaptions.captionedimage')),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtailmetadata.models.WagtailImageMetadataMixin, 'wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='BlogTagIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='FormPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.page')),
                ('to_address', models.CharField(max_length=255)),
                ('from_address', models.EmailField(max_length=255)),
                ('subject', models.CharField(max_length=255)),
                ('intro', wagtail.fields.RichTextField()),
                ('thank_you_text', wagtail.fields.RichTextField()),
                ('contact_title', models.CharField(max_length=255)),
                ('contact_description', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=(wagtail.contrib.forms.models.FormMixin, 'wagtailcore.page', models.Model),
        ),
        migrations.CreateModel(
            name='IpAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('ip_address', models.GenericIPAddressField()),
                ('country', models.CharField(max_length=100)),
                ('city', models.CharField(default='Unknown', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_visit', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('taggit.tag',),
        ),
        migrations.CreateModel(
            name='FormField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('sort_order', models.IntegerField(null=True)),
                ('clean_name', models.CharField(default='', max_length=255)),
                ('label', models.CharField(max_length=255)),
                ('field_type', models.CharField(choices=[('singleline', 'Single line text'), ('multiline', 'Multi-line text'), ('email', 'Email'), ('number', 'Number'), ('url', 'URL'), ('checkbox', 'Checkbox'), ('checkboxes', 'Checkboxes'), ('dropdown', 'Drop down'), ('multiselect', 'Multiple select'), ('radio', 'Radio buttons'), ('date', 'Date'), ('datetime', 'Date/time'), ('hidden', 'Hidden field')], max_length=16)),
                ('required', models.BooleanField(default=True)),
                ('choices', models.TextField()),
                ('default_value', models.TextField()),
                ('help_text', models.CharField(max_length=255)),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='form_fields', to='blog.formpage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('body', models.TextField()),
                ('session_key', models.CharField(max_length=40)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.blogpage')),
            ],
        ),
        migrations.CreateModel(
            name='BlogPageTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('content_object', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='tagged_items', to='blog.blogpage')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_items', to='taggit.tag')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BlogPageGalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('sort_order', models.IntegerField(null=True)),
                ('caption', models.CharField(max_length=250)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='wagtailimages.image')),
                ('page', modelcluster.fields.ParentalKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_images', to='blog.blogpage')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='blogpage',
            name='tags',
            field=modelcluster.contrib.taggit.ClusterTaggableManager(through='blog.BlogPageTag', to='taggit.Tag'),
        ),
    ]
