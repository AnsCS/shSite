# from wagtail.blocks import (
#     BooleanBlock,
#     CharBlock,
#     ChoiceBlock,
#     DateTimeBlock,
#     FieldBlock,
#     IntegerBlock,
#     ListBlock,
#     PageChooserBlock,
#     RawHTMLBlock,
#     RichTextBlock,
#     StreamBlock,
#     StructBlock,
#     StructValue,
#     TextBlock,
#     URLBlock,
# )

# # test
# from wagtail.embeds.blocks import EmbedBlock
# from wagtail.images.api.fields import ImageRenditionField
# from wagtail.images.blocks import ImageChooserBlock
# from wagtail.snippets.blocks import SnippetChooserBlock
# #end test
# class ImageText(StructBlock):
#     reverse = BooleanBlock(required=False)
#     text = RichTextBlock()
#     image = ImageChooserBlock()

# class BodyBlock(StreamBlock):
#     h1 = CharBlock()
#     h2 = CharBlock()
#     paragraph = RichTextBlock()
#     image_text = ImageText()
#     image_carousel = ListBlock(ImageChooserBlock())
#     thumbnail_gallery = ListBlock(ImageChooserBlock())

# #end class test