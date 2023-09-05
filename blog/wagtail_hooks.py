from wagtail import blocks, hooks
import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail.admin.rich_text.converters.html_to_contentstate import InlineStyleElementHandler
from .models import BlogPage

from django.utils.safestring import mark_safe

from wagtail.admin.ui.components import Component

from wagtail.contrib.modeladmin.options import modeladmin_register
# from home.models import SurveyPage  # your survejs page model
from wagtailsurveyjs.wagtail_hooks import BaseSurveyModelAdmin


# class SurveyModelAdmin(BaseSurveyModelAdmin):
#     model = SurveyPage
#     menu_label = 'Surveys'
#     menu_icon = 'folder-inverse'
#     menu_order = 700


# modeladmin_register(SurveyModelAdmin)


# تعديل الدالة لتخزين المعلومات الإضافية
@hooks.register('page_view')
def log_page_view(request, page):
    # تخزين المعلومات في قاعدة البيانات
    PageView.objects.create(
        page=page,
        ip=get_client_ip(request),
        url=request.build_absolute_uri()
    )
# دالة مساعدة للحصول على عنوان IP الخاص بالعميل
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip



# class WelcomePanel(Component):
#     order = 50

#     def render_html(self, parent_context):
#         return mark_safe("""
#         <section class="panel summary nice-padding">
#           <h3>No, but seriously -- welcome to the admin homepage.</h3>
#         </section>
#         """)

# @hooks.register('construct_homepage_panels')
# def add_another_welcome_panel(request, panels):
#     panels.append(WelcomePanel())


from django.contrib.gis.geoip2 import GeoIP2
# from .models import SiteVisitCount

# @hooks.register('before_serve_page')
# def update_visit_count(page, request, serve_args, serve_kwargs):
#     # Get the visitor's country from their IP address
#     ip = request.META.get('REMOTE_ADDR')
#     if ip and ip != '127.0.0.1':
#         g = GeoIP2('blog/templates/GeoLite2-Country.mmdb')
#         country = g.country(ip)['country_name']
#     else:
#         country = None

#     # Increment the visit count and pass the country value
#     SiteVisitCount.increment(country=country)

# # # visit count in BlogPage - Blgo app
# # @hooks.register('before_serve_page')
# # def update_visit_count(page, request, serve_args, serve_kwargs):
# #     SiteVisitCount.increment()


# # @hooks.register('before_serve_page')
# # def update_visit_count(page, request, serve_args, serve_kwargs):
# #     if isinstance(page, BlogPage):
# #         page.visit_count += 1
# #         page.save(update_fields=['visit_count'])

# View count in BlogPage - Blgo app
@hooks.register('before_serve_page')
def increment_view_count(page, request, serve_args, serve_kwargs):
    if isinstance(page, BlogPage):
        viewed_pages = request.session.get('viewed_pages', [])
        if page.pk not in viewed_pages:
            page.view_count += 1
            page.save()
            viewed_pages.append(page.pk)
            request.session['viewed_pages'] = viewed_pages


# from .models import VisitIp

# @hooks.register('before_serve_page')
# def update_visit_ip(request, page, serve_args, serve_kwargs):
#     if isinstance(page, BlogPage):
#         ip = request.META.get('REMOTE_ADDR')
#         url = request.build_absolute_uri()
#         visit_ip, created = VisitIp.objects.get_or_create(ip=ip, url=url)
#         # هنا يمكنك تحديث قيمة time_spent في قاعدة البيانات




@hooks.register("register_rich_text_features")
def register_centertext_feature(features):
    """Creates centered text in our richtext editor and page."""

    # Step 1
    feature_name = "center"
    type_ = "CENTERTEXT"
    tag = "div"

    # Step 2
    control = {
        "type": type_,
        "label": "Center",
        "description": "Center Text",
        "style": {
            "display": "block",
            "text-align": "center",
        },
    }

    # Step 3
    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    # Step 4
    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {
            "style_map": {
                type_: {
                    "element": tag,
                    "props": {
                        "class": "d-block text-center"
                    }
                }
            }
        }
    }

    # Step 5
    features.register_converter_rule("contentstate", feature_name, db_conversion)

    # Step 6, This is optional.
    features.default_features.append(feature_name)

# @hooks.register('register_rich_text_features')
# def register_mark_feature(features):
#     """
#     Registering the `mark` feature, which uses the `MARK` Draft.js inline style type,
#     and is stored as HTML with a `<mark>` tag.
#     """
#     feature_name = 'mark'
#     type_ = 'MARK'
#     tag = 'mark'

#     # 2. Configure how Draftail handles the feature in its toolbar.
#     control = {
#         'type': type_,
#         'label': '☆',
#         'description': 'Mark',
#         'style': {'backgroundColor': 'yellow'},
#         'element': 'mark',
#     }

#     # 3. Call register_editor_plugin to register the configuration for Draftail.
#     features.register_editor_plugin(
#         'draftail', feature_name, draftail_features.InlineStyleFeature(control)
#     )

#     # 4.configure the content transform from the DB to the editor and back.
#     db_conversion = {
#         'from_database_format': {tag: InlineStyleElementHandler(type_)},
#         'to_database_format': {'style_map': {type_: {'element': tag}}},
#     }

#     # 5. Call register_converter_rule to register the content transformation conversion.
#     features.register_converter_rule('contentstate', feature_name, db_conversion)

#     # 6. (optional) Add the feature to the default features list to make it available
#     # on rich text fields that do not specify an explicit 'features' list
#     features.default_features.append('mark')


# 1. Use the register_rich_text_features hook.
@hooks.register('register_rich_text_features')
def register_mark_feature(features):
    """
    Registering the `mark` feature, which uses the `MARK` Draft.js inline style type,
    and is stored as HTML with a `<mark>` tag.
    """
    feature_name = 'mark'
    type_ = 'MARK'
    tag = 'mark'

    # 2. Configure how Draftail handles the feature in its toolbar.
    control = {
        'type': type_,
        'label': '☆',
        'description': 'Mark',
        # This isn’t even required – Draftail has predefined styles for MARK.
        # 'style': {'textDecoration': 'line-through'},
    }

    # 3. Call register_editor_plugin to register the configuration for Draftail.
    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    # 4.configure the content transform from the DB to the editor and back.
    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {type_: tag}},
    }

    # 5. Call register_converter_rule to register the content transformation conversion.
    features.register_converter_rule('contentstate', feature_name, db_conversion)

    # 6. (optional) Add the feature to the default features list to make it available
    # on rich text fields that do not specify an explicit 'features' list
    features.default_features.append('mark')



# 1. Use the register_rich_text_features hook.
@hooks.register('register_rich_text_features')
def register_mark_feature(features):
    """
    Registering the `mark` feature, which uses the `MARK` Draft.js inline style type,
    and is stored as HTML with a `<mark>` tag.
    """
    feature_name = 'h6'
    type_ = 'H6'
    tag = 'h6'

    # 2. Configure how Draftail handles the feature in its toolbar.
    control = {
        'type': type_,
        'label': 'H5',
        'description': 'h6',
        # This isn’t even required – Draftail has predefined styles for h6.
        # 'style': {'textDecoration': 'line-through'},
    }

    # 3. Call register_editor_plugin to register the configuration for Draftail.
    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    # 4.configure the content transform from the DB to the editor and back.
    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {type_: tag}},
    }

    # 5. Call register_converter_rule to register the content transformation conversion.
    features.register_converter_rule('contentstate', feature_name, db_conversion)

    # 6. (optional) Add the feature to the default features list to make it available
    # on rich text fields that do not specify an explicit 'features' list
    features.default_features.append('h6')

# 1. Use the register_rich_text_features hook.
@hooks.register('register_rich_text_features')
def register_mark_feature(features):
    """
    Registering the `mark` feature, which uses the `MARK` Draft.js inline style type,
    and is stored as HTML with a `<mark>` tag.
    """
    feature_name = 'h5'
    type_ = 'H5'
    tag = 'h5'

    # 2. Configure how Draftail handles the feature in its toolbar.
    control = {
        'type': type_,
        'label': 'H5',
        'description': 'h5',
        # This isn’t even required – Draftail has predefined styles for h6.
        # 'style': {'textDecoration': 'line-through'},
    }

    # 3. Call register_editor_plugin to register the configuration for Draftail.
    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    # 4.configure the content transform from the DB to the editor and back.
    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {type_: tag}},
    }

    # 5. Call register_converter_rule to register the content transformation conversion.
    features.register_converter_rule('contentstate', feature_name, db_conversion)

    # 6. (optional) Add the feature to the default features list to make it available
    # on rich text fields that do not specify an explicit 'features' list
    features.default_features.append('h5')


# 1. Use the register_rich_text_features hook.
@hooks.register('register_rich_text_features')
def register_mark_feature(features):
    """
    Registering the `mark` feature, which uses the `MARK` Draft.js inline style type,
    and is stored as HTML with a `<mark>` tag.
    """
    feature_name = 'h1'
    type_ = 'H1'
    tag = 'h1'

    # 2. Configure how Draftail handles the feature in its toolbar.
    control = {
        'type': type_,
        'label': 'H1',
        'description': 'h1',
        # This isn’t even required – Draftail has predefined styles for h6.
        # 'style': {'textDecoration': 'line-through'},
    }

    # 3. Call register_editor_plugin to register the configuration for Draftail.
    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    # 4.configure the content transform from the DB to the editor and back.
    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {type_: tag}},
    }

    # 5. Call register_converter_rule to register the content transformation conversion.
    features.register_converter_rule('contentstate', feature_name, db_conversion)

    # 6. (optional) Add the feature to the default features list to make it available
    # on rich text fields that do not specify an explicit 'features' list
    features.default_features.append('h1')


@hooks.register('register_rich_text_features')
def register_small_feature(features):
    """
    Registering the `small` feature, which uses the `SMALL` Draft.js inline style type,
    and is stored as HTML with a `<small>` tag.
    """
    feature_name = 'small'
    type_ = 'SMALL'
    tag = 'small'

    # 2. Configure how Draftail handles the feature in its toolbar.
    control = {
        'type': type_,
        'label': 'SMALL',
        'description': 'Small',
        'element': 'small',
    }

    # 3. Call register_editor_plugin to register the configuration for Draftail.
    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    # 4.configure the content transform from the DB to the editor and back.
    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {type_: {'element': tag}}},
    }

    # 5. Call register_converter_rule to register the content transformation conversion.
    features.register_converter_rule('contentstate', feature_name, db_conversion)

    # 6. (optional) Add the feature to the default features list to make it available
    # on rich text fields that do not specify an explicit 'features' list
    features.default_features.append(feature_name)




@hooks.register('register_rich_text_features')
def register_small_feature(features):
    """
    Registering the `small` feature, which uses the `SMALL` Draft.js inline style type,
    and is stored as HTML with a `<small>` tag.
    """
    feature_name = 'sub'
    type_ = 'sub'
    tag = 'sub'

    # 2. Configure how Draftail handles the feature in its toolbar.
    control = {
        'type': type_,
        'label': 'sub',
        'description': 'sub',
        'element': 'sub',
    }

    # 3. Call register_editor_plugin to register the configuration for Draftail.
    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    # 4.configure the content transform from the DB to the editor and back.
    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {type_: {'element': tag}}},
    }

    # 5. Call register_converter_rule to register the content transformation conversion.
    features.register_converter_rule('contentstate', feature_name, db_conversion)

    # 6. (optional) Add the feature to the default features list to make it available
    # on rich text fields that do not specify an explicit 'features' list
    features.default_features.append(feature_name)



@hooks.register('register_rich_text_features')
def register_small_feature(features):
    """
    Registering the `small` feature, which uses the `SMALL` Draft.js inline style type,
    and is stored as HTML with a `<small>` tag.
    """
    feature_name = 's'
    type_ = 'S'
    tag = 's'

    # 2. Configure how Draftail handles the feature in its toolbar.
    control = {
        'type': type_,
        'label': 's',
        'description': 's',
        'element': 's',
    }

    # 3. Call register_editor_plugin to register the configuration for Draftail.
    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    # 4.configure the content transform from the DB to the editor and back.
    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {type_: {'element': tag}}},
    }

    # 5. Call register_converter_rule to register the content transformation conversion.
    features.register_converter_rule('contentstate', feature_name, db_conversion)

    # 6. (optional) Add the feature to the default features list to make it available
    # on rich text fields that do not specify an explicit 'features' list
    features.default_features.append(feature_name)


@hooks.register('register_rich_text_features')
def register_small_feature(features):
    """
    Registering the `small` feature, which uses the `SMALL` Draft.js inline style type,
    and is stored as HTML with a `<small>` tag.
    """
    feature_name = 'pre'
    type_ = 'pre'
    tag = 'pre'

    # 2. Configure how Draftail handles the feature in its toolbar.
    control = {
        'type': type_,
        'label': 'pre',
        'description': 'pre',
        'element': 'pre',
    }

    # 3. Call register_editor_plugin to register the configuration for Draftail.
    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    # 4.configure the content transform from the DB to the editor and back.
    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {type_: {'element': tag}}},
    }

    # 5. Call register_converter_rule to register the content transformation conversion.
    features.register_converter_rule('contentstate', feature_name, db_conversion)

    # 6. (optional) Add the feature to the default features list to make it available
    # on rich text fields that do not specify an explicit 'features' list
    features.default_features.append(feature_name)

@hooks.register('register_rich_text_features')
def register_small_feature(features):
    """
    Registering the `small` feature, which uses the `SMALL` Draft.js inline style type,
    and is stored as HTML with a `<small>` tag.
    """
    feature_name = 'kbd'
    type_ = 'kbd'
    tag = 'kbd'

    # 2. Configure how Draftail handles the feature in its toolbar.
    control = {
        'type': type_,
        'label': 'kbd',
        'description': 'kbd',
        'element': 'kbd',
    }

    # 3. Call register_editor_plugin to register the configuration for Draftail.
    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    # 4.configure the content transform from the DB to the editor and back.
    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {type_: {'element': tag}}},
    }

    # 5. Call register_converter_rule to register the content transformation conversion.
    features.register_converter_rule('contentstate', feature_name, db_conversion)

    # 6. (optional) Add the feature to the default features list to make it available
    # on rich text fields that do not specify an explicit 'features' list
    features.default_features.append(feature_name)


@hooks.register('register_rich_text_features')
def register_small_feature(features):
    """
    Registering the `small` feature, which uses the `SMALL` Draft.js inline style type,
    and is stored as HTML with a `<small>` tag.
    """
    feature_name = 'hgroup'
    type_ = 'hgroup'
    tag = 'hgroup'

    # 2. Configure how Draftail handles the feature in its toolbar.
    control = {
        'type': type_,
        'label': 'hgroup',
        'description': 'hgroup',
        'element': 'hgroup',
    }

    # 3. Call register_editor_plugin to register the configuration for Draftail.
    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    # 4.configure the content transform from the DB to the editor and back.
    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {type_: {'element': tag}}},
    }

    # 5. Call register_converter_rule to register the content transformation conversion.
    features.register_converter_rule('contentstate', feature_name, db_conversion)

    # 6. (optional) Add the feature to the default features list to make it available
    # on rich text fields that do not specify an explicit 'features' list
    features.default_features.append(feature_name)

####################################################################
@hooks.register('register_rich_text_features')
def register_small_feature(features):
    """
    Registering the `small` feature, which uses the `SMALL` Draft.js inline style type,
    and is stored as HTML with a `<small>` tag.
    """
    feature_name = 'code'
    type_ = 'code'
    tag = 'code'

    # 2. Configure how Draftail handles the feature in its toolbar.
    control = {
        'type': type_,
        'label': 'code',
        'description': 'code',
        'element': 'code',
    }

    # 3. Call register_editor_plugin to register the configuration for Draftail.
    features.register_editor_plugin(
        'draftail', feature_name, draftail_features.InlineStyleFeature(control)
    )

    # 4.configure the content transform from the DB to the editor and back.
    db_conversion = {
        'from_database_format': {tag: InlineStyleElementHandler(type_)},
        'to_database_format': {'style_map': {type_: {'element': tag}}},
    }

    # 5. Call register_converter_rule to register the content transformation conversion.
    features.register_converter_rule('contentstate', feature_name, db_conversion)

    # 6. (optional) Add the feature to the default features list to make it available
    # on rich text fields that do not specify an explicit 'features' list
    features.default_features.append(feature_name)





@hooks.register("register_rich_text_features")
def register_righttext_feature(features):
    """Creates right aligned text in our richtext editor and page."""

    # Step 1
    feature_name = "right"
    type_ = "RIGHTTEXT"
    tag = "span"

    # Step 2
    control = {
        "type": type_,
        "label": "Right",
        "direction": "rtl",
        "style": {
            "display": "block",
            "text-align": "right",
        },
    }

    # Step 3
    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    # Step 4
    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {
            "style_map": {
                type_: {
                    "element": tag,
                    "props": {
                        "class": "richtext-right"
                    }
                }
            }
        }
    }

    # Step 5
    features.register_converter_rule("contentstate", feature_name, db_conversion)

    # Step 6, This is optional.
    features.default_features.append(feature_name)

@hooks.register("register_rich_text_features")
def register_lefttext_feature(features):
    """Creates left aligned text in our richtext editor and page."""

    # Step 1
    feature_name = "left"
    type_ = "LEFTTEXT"
    tag = "span"

    # Step 2
    control = {
        "type": type_,
        "label": "Left",
        "description": "ltr",
        "style": {
            "display": "block",
            "text-align": "left",
        },
    }

    # Step 3
    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    # Step 4
    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {
            "style_map": {
                type_: {
                    "element": tag,
                    "props": {
                        "class": "richtext-left"
                    }
                }
            }
        }
    }

    # Step 5
    features.register_converter_rule("contentstate", feature_name, db_conversion)

    # Step 6, This is optional.
    features.default_features.append(feature_name)

# @hooks.register("register_rich_text_features")
# def register_righttext_feature(features):
#     """Creates right aligned text in our richtext editor and page."""

#     # Step 1
#     feature_name = "right"
#     type_ = "RIGHTTEXT"
#     tag = "div"

#     # Step 2
#     control = {
#         "type": type_,
#         "label": "Right",
#         "description": "Right Align Text",
#         "style": {
#             "display": "block",
#             "text-align": "right",
#         },
#     }

#     # Step 3
#     features.register_editor_plugin(
#         "draftail", feature_name, draftail_features.InlineStyleFeature(control)
#     )

#     # Step 4
#     db_conversion = {
#         "from_database_format": {tag: InlineStyleElementHandler(type_)},
#         "to_database_format": {
#             "style_map": {
#                 type_: {
#                     "element": tag,
#                     "props": {
#                         "class": "d-block text-right"
#                     }
#                 }
#             }
#         }
#     }

#     # Step 5
#     features.register_converter_rule("contentstate", feature_name, db_conversion)

#     # Step 6, This is optional.
#     features.default_features.append(feature_name)