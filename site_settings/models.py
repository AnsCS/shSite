from django.db import models

# Create your models here.
from wagtail.admin.panels import(
    FieldPanel, InlinePanel,
    MultiFieldPanel, FieldRowPanel
    )
from wagtail.contrib.settings.models import (
    BaseGenericSetting,
    BaseSiteSetting,
    register_setting,
)

@register_setting
class SocialMediaSettings(BaseGenericSetting ):
    """Social media settings for our custom website."""

    facebook = models.URLField(blank=True, null=True, help_text="Facebook URL")
    twitter = models.URLField(blank=True, null=True, help_text="Twitter URL")
    instagram = models.URLField(blank=True, null=True, help_text="instagram URL")
    telegram = models.URLField(blank=True, null=True, help_text="telegram Channel URL")
    youtube = models.URLField(blank=True, null=True, help_text="YouTube Channel URL")

    panels = [
        MultiFieldPanel([
            FieldPanel("facebook"),
            FieldPanel("twitter"),
            FieldPanel("instagram"),
            FieldPanel("telegram"),
            FieldPanel("youtube"),
        ], heading="Social Media Settings")
    ]