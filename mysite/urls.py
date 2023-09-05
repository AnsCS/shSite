from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.contrib.sitemaps.views import sitemap
# from blog.views import SearchView
from search import views as search_views
import blog.urls
# from blog.views import cached_serve

from blog.api import api_router

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("", include(blog.urls)),
    path("", include("home.urls")),


    path("ckeditor5/", include('django_ckeditor_5.urls')),
    # path('summernote/', include('django_summernote.urls')), # Delete

   # This line MUST come before the bottom url pattern
    path('api/v2/', api_router.urls),

    path("__debug__/", include("debug_toolbar.urls")),

    # path('search/', SearchView.as_view(), name='search'),
    # path("", cached_serve, name="wagtail_serve"),

    path('sitemap.xml/', sitemap),
    # code omitted for brevity
    path('comments/', include('django_comments.urls')),

]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = urlpatterns + i18n_patterns(
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("search/", search_views.search, name="search"),
    path("", include(wagtail_urls)),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
)
