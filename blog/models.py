from django import forms
from django.db import models
from django.template.loader import render_to_string
from django.views.generic import TemplateView
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase
from wagtail.embeds.blocks import EmbedBlock
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import(
    FieldPanel, InlinePanel,
    MultiFieldPanel, FieldRowPanel
    )
from wagtail.search import index
from django.shortcuts import redirect
from wagtail.snippets.models import register_snippet
import json
import requests
from django.conf import settings
from django.http import HttpResponse
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.fields import StreamField
from django_ckeditor_5.fields import CKEditor5Field
from django import forms
#test
# from .blocks import BodyBlock
#endtest
from wagtailmetadata.models import MetadataPageMixin
from wagtail.api import APIField
from wagtailautocomplete.edit_handlers import AutocompletePanel
from wagtail.blocks import StreamBlock
from wagtail.contrib.table_block.blocks import TableBlock
from wagtail.blocks import (
    RawHTMLBlock, BlockQuoteBlock,
    ChoiceBlock, StructBlock
    )
# from wagtail.blocks import (
#     RawHTMLBlock, BlockQuoteBlock,
#     ChoiceBlock, StructBlock
#     )
from wagtail.contrib.forms.models import (
    AbstractEmailForm, AbstractFormField
    )
from wagtailcaptcha.models import WagtailCaptchaEmailForm
from django.utils.functional import cached_property
from wagtail.contrib.forms.views import SubmissionsListView

class CustomSubmissionsListView(SubmissionsListView):
    paginate_by = 50  # show more submissions per page, default is 20
    ordering = ('submit_time',)  # order submissions by oldest first, normally newest first
    ordering_csv = ('-submit_time',)  # order csv export by newest first, normally oldest first

    # override the method to generate csv filename
    def get_csv_filename(self):
        """ Returns the filename for CSV file with page slug at start"""
        filename = super().get_csv_filename()
        return self.form_page.slug + '-' + filename

class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')

class FormPage(WagtailCaptchaEmailForm, AbstractEmailForm):
    """Form Page with customised submissions listing view"""

    # set custom view class as class attribute
    submissions_list_view_class = CustomSubmissionsListView

    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    contact_title = models.CharField(max_length=255, blank=True) # إضافة هذا السطر
    contact_description = models.CharField(max_length=255, blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        FieldPanel('contact_title'), # وهذا السطر
        FieldPanel('contact_description'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]

class BlogIndexPage(Page): #                                                                  IMPORT
    intro = RichTextField(blank=True)

    def get_sitemap_urls(self, request=None):
        return []

    def get_recent_blogs(self):
        # استرجاع المنشورات الأخيرة
        recent_blogs = BlogPage.objects.live().order_by('-first_published_at')
        return recent_blogs

    def get_context(self, request):
        context = super().get_context(request)
        # إضافة المنشورات الأخيرة إلى السياق
        context['recent_blogs'] = self.get_recent_blogs()
        return context
    # Add the main_image method:
    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    def get_sitemap_urls(self, request=None):
        return []

    def get_recent_blogs(self):
        # استرجاع المنشورات الأخيرة
        recent_blogs = BlogPage.objects.live().order_by('-first_published_at')
        return recent_blogs

    def get_tags(self):
        # استرجاع جميع العلامات المستخدمة
        tags = BlogPageTag.objects.all().values_list('tag__name', flat=True).distinct()
        return tags

    def get_context(self, request):
        context = super().get_context(request)
        # إضافة المنشورات الأخيرة والعلامات إلى السياق
        context['recent_blogs'] = self.get_recent_blogs()
        context['tags'] = self.get_tags()
        return context

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]
# ... (Keep the definition of BlogIndexPage)


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )



# class BlogIndexPage(Page):
#     intro = RichTextField(blank=True)

#     def get_context(self, request):
#         # Update context to include only published posts, ordered by reverse-chron
#         context = super().get_context(request)
#         blogpages = self.get_children().live().order_by('-first_published_at')
#         context['blogpages'] = blogpages
#         return context

class BlogTagIndexPage(Page):

    site_settings = models.ForeignKey(
        "blog.SiteSettings",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    content_panels = Page.content_panels + [
        # ...
        FieldPanel("site_settings"),
    ]

    def __str__(self):
        return self.site_settings

    def get_tags(self):
        # استرجاع جميع العلامات المستخدمة
        tags = BlogPageTag.objects.all().values_list('tag__name', flat=True).distinct()
        return tags

    def get_context(self, request):
        # Filter by tag
        tag = request.GET.get('tag')
        blogpages = BlogPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['blogpages'] = blogpages
        context['tags'] = self.get_tags()
        return context
    def __str__(self):
        return str(self.site_settings)



class VideoBlock(blocks.StructBlock):
    url = blocks.URLBlock()
    max_width = blocks.IntegerBlock(default=1094, min_value=100, max_value=1400)
    max_height = blocks.IntegerBlock(default=529, min_value=100, max_value=1000)
    title = blocks.CharBlock(required=False)
class AlignedTextBlock(blocks.StructBlock):
    text = blocks.RichTextBlock()
    alignment = blocks.ChoiceBlock(choices=[
        ('left', 'Left'),
        ('center', 'Center'),
        ('right', 'Right'),
    ], default='left')

class CodeBlock(blocks.StructBlock):
    code = blocks.TextBlock()
    language = blocks.CharBlock(required=False, help_text='Programming language (e.g. python, javascript)')

class SearchForm(forms.Form):
    query = forms.CharField()

class CustomImageBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False)
    image_url = blocks.URLBlock(required=False)
    caption = blocks.CharBlock(required=False, max_length=255)



class IngredientBlock(blocks.StructBlock):
    ingredient = blocks.CharBlock()
    amount = blocks.CharBlock(required=False)

class RecipeBlock(blocks.StructBlock):
    title = blocks.CharBlock()
    ingredients = blocks.ListBlock(IngredientBlock)
    instructions = blocks.RichTextBlock()

class BlockQuoteBlock(blocks.StructBlock):
    text = blocks.TextBlock(required=True)
    name = blocks.CharBlock(required=False)

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
# class DemoStreamBlock(StreamBlock):
#     table = TableBlock(table_options=new_table_options)


from wagtailsurveyjs.models import AbstractSurveyJsFormPage

from wagtailtables.blocks import TableBlock
TOOLBAR = [
    {'type': 'i', 'content': 'format_align_left', 'k': 'text-align', 'v': 'left'},
    {'type': 'i', 'content': 'format_align_center', 'k':'text-align', 'v':'center'},
    {'type': 'i', 'content': 'format_align_right', 'k': 'text-align', 'v': 'right'},
    {'type': 'i', 'content': 'format_bold', 'k': 'font-weight', 'v': '600'},
    {'type': 'i', 'content': 'format_italic', 'k': 'font-style', 'v': 'italic'},
    {'type': 'i', 'content': 'border_left', 'k': 'border-left', 'v': '1px solid'},
    {'type': 'i', 'content': 'border_right', 'k': 'border-right', 'v': '1px solid'},
    {'type': 'i', 'content': 'border_top', 'k': 'border-top', 'v': '1px solid'},
    {'type': 'i', 'content': 'format_size', 'k': 'font-size', 'v': '16px'}
]

class ContentBlocks(StreamBlock):
    table_block = TableBlock(toolbar=TOOLBAR)


class BlogPage(MetadataPageMixin, Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = CKEditor5Field('body', config_name='extends',  blank=True)

    summary = RichTextField(blank=True)
    view_count = models.PositiveIntegerField(default=0)
    # visit_count = models.PositiveIntegerField(default=0)

    show_body = StreamField([
        # ('heading', blocks.CharBlock()),

        ('heading', blocks.StructBlock([
        ('text', blocks.CharBlock()),
        ('alignment', blocks.ChoiceBlock(choices=[
            ('left', 'Left'),
            ('center', 'Center'),
            ('right', 'Right'),
            ], icon='cup')),
        ])),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
        ('video', VideoBlock()),
        ('aligned_text', AlignedTextBlock()),
        ('code', CodeBlock()),
        ('raw_html', RawHTMLBlock()),
        ('blockquote', BlockQuoteBlock()),
        # ('table' , DemoStreamBlock()),
        ('tables', ContentBlocks()),

        ('person', blocks.StructBlock([
            ('name', blocks.CharBlock()),
            ('fullName_color', blocks.TextBlock(required=False, help_text="Hexadecimal, rgba, or CSS color notation (e.g. #ff0011)")),
            ('pe_image', ImageChooserBlock()),
            ('biography', blocks.RichTextBlock()),
            ('text_color', blocks.TextBlock(required=False, help_text="Hexadecimal, rgba, or CSS color notation (e.g. #ff0011)")),
            ('background_color', blocks.TextBlock(required=False, help_text="Hexadecimal, rgba, or CSS color notation (e.g. #ff0011)")),
            ('description', blocks.StreamBlock([
                ('description_item', blocks.RichTextBlock(required=False))
                ], required=False))
            ], icon='user')),
        ('recipe', RecipeBlock()),
        ('note', blocks.StructBlock([
        ('title', blocks.CharBlock()),
        ('description', blocks.RichTextBlock())
    ])),
    ], use_json_field=True, blank=False, null=True)

    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)

    site_settings = models.ForeignKey(
        "blog.SiteSettings",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    featured_image = models.ForeignKey(
        'wagtailimagecaptions.CaptionedImage',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='Featured Image'
    )
    api_fields = [ # for API v2
            APIField("intro"),
            APIField("date"),
            APIField("summary"),
            APIField("categories"),
            APIField("body"),
            APIField("view_count"),
            APIField("show_body"),
            APIField("tags"),
            APIField("featured_image"),
        ]

    def serve(self, request, *args, **kwargs):
        # زيادة عدد الزيارات
        self.visit_count += 1
        self.save()

        return super().serve(request, *args, **kwargs)

    def get_popular_pages_from_database():
        # استخدم QuerySet API لجلب الصفحات الأكثر زيارة
        popular_pages = BlogPage.objects.order_by('-visit_count')

        # قم بتنسيق الإحصاءات كما تريد عرضها
        formatted_stats = ""
        for page in popular_pages:
            formatted_stats += f"{page.title}: {page.visit_count}<br>"

        return formatted_stats

    def get_admin_display_title(self):
        return f"{self.title} ({self.view_count} views)"

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['search_form'] = SearchForm()
        return context

    def get_context(self, request):
        context = super().get_context(request)
        context['comments'] = Comment.objects.filter(post=self)
        return context

    def serve(self, request):
        if request.method == 'POST':
            # Get the reCAPTCHA response from the form data
            recaptcha_response = request.POST.get('g-recaptcha-response')
            # Verify the reCAPTCHA response using the secret key
            data = {
                'secret': settings.RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = json.loads(r.text)
            # Check if the reCAPTCHA response is valid
            if result['success']:
                # The reCAPTCHA response is valid, process the comment
                if not request.session.session_key:
                    request.session.save()
                comment = Comment(
                    post=self,
                    name=request.POST.get('name'),
                    email=request.POST.get('email'),
                    body=request.POST.get('body'),
                    session_key=request.session.session_key
                )
                comment.save()
                return redirect(request.path)
            else:
                # The reCAPTCHA response is not valid, show an error message
                context = self.get_context(request)
                context['recaptcha_error'] = "Please complete the reCAPTCHA."
                html = render_to_string('blog/blog_page.html', context)
                return HttpResponse(html)
        else:
            return super().serve(request)

    # def get_context(self, request):
    #     context = super().get_context(request)
    #     comments = Comment.objects.filter(post=self)

    #     # Get the current user's session key
    #     user_session_key = request.session.session_key

    #     # Filter the comments by the session key
    #     user_comments = comments.filter(session_key=user_session_key)
    #     other_comments = comments.exclude(session_key=user_session_key)

    #     # Pass the two lists to the template context
    #     context['user_comments'] = user_comments
    #     context['other_comments'] = other_comments

    #     return context
    def get_context(self, request):
        context = super().get_context(request)
        comments = Comment.objects.filter(post=self)

        # Get the current user's session key
        user_session_key = request.session.session_key

        # Filter the comments by the session key
        user_comments = comments.filter(session_key=user_session_key)
        other_comments = comments.exclude(session_key=user_session_key)

        # Add a flag to show or hide the edit and delete buttons for each user comment
        for comment in user_comments:
            if comment.session_key == user_session_key:
                comment.show_buttons = True
            else:
                comment.show_buttons = False

        # Pass the two lists to the template context
        context['user_comments'] = user_comments
        context['other_comments'] = other_comments

        return context


    def get_related_posts(self):
        # الحصول على قائمة العلامات المرتبطة بهذه الصفحة
        tags = self.tags.all()

        # البحث عن المنشورات التي تحتوي على أي من هذه العلامات
        related_posts = BlogPage.objects.filter(tags__in=tags).exclude(id=self.id)

        # إرجاع أول 3 منشورات فقط
        return related_posts[:3]

    search_fields = Page.search_fields + [
        index.SearchField('title'),
        index.SearchField('intro'),
        # index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Blog information"),
        FieldPanel('intro'),

        FieldPanel('body'),
        FieldPanel('show_body'),
        InlinePanel('gallery_images', label="Gallery images"),
        FieldPanel('featured_image'),
        FieldPanel('summary'),

        # FieldPanel('body_test'),
    ]
class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimagecaptions.CaptionedImage', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimagecaptions.CaptionedImage', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )
    api_fields = [
        APIField('name'),
        APIField('icon'),

    ]

    panels = [
        FieldPanel('name'),
        FieldPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'blog categories'

from taggit.models import Tag as TaggitTag

@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True

@register_snippet
class Comment(models.Model):
    post = models.ForeignKey(BlogPage, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    session_key = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)

    api_fields = [
        APIField('post'),
        APIField('name'),
        APIField('body'),
    ]

    panels = [
        FieldPanel('post'),
        FieldPanel('name'),
        FieldPanel('email'),
        FieldPanel('body'),
    ]

    def __str__(self):
        return self.name


# from django.utils import timezone


from django.utils import timezone



class IpAddress(models.Model):
    ip_address = models.GenericIPAddressField()
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, default='Unknown')
    created_at = models.DateTimeField(auto_now_add=True)
    last_visit = models.DateField(auto_now=True)


    def __str__(self):
        return self.ip_address



from django.contrib.sessions.models import Session


@register_snippet
class SiteSettings(models.Model):
    read_more_text = models.CharField(max_length=255, default="Read more")
    text_alignment = models.CharField(
        max_length=255,
        choices=[("left", "Left"), ("center", "Center"), ("right", "Right")],
        default="left",
    )


    panels = [
        FieldPanel("read_more_text"),
        FieldPanel("text_alignment"),
    ]
    class Meta:
        verbose_name = "Site Settings"

    def __str__(self):
        return self.read_more_text

