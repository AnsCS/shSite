from django.urls import path, re_path
from . import views
from django.urls import path, include
from rest_framework import routers
# from blog.views import BlogCategoryViewSet
from .models import BlogCategory
# router = routers.DefaultRouter()
# router.register(r'blogcategories', BlogCategoryViewSet)
# from rest_framework import routers
from .views import BlogPageViewSet, BlogCategoryViewSet, CommentViewSet
from django.urls import path, include
# from .views import BlogPageViewSet, BlogCategoryViewSet , visits_by_country
# from .views import VisitIpViewSet

router = routers.DefaultRouter()
router.register(r'blogpages', BlogPageViewSet)
router.register(r'blogcategories', BlogCategoryViewSet)
router.register(r'comments', CommentViewSet, basename='comment')

# router = routers.DefaultRouter()
# router.register(r'visits', VisitIpViewSet)
from wagtail.api.v2.router import WagtailAPIRouter
from .views import CommentAPIViewSet
from .api import api_router

# api_router = WagtailAPIRouter('wagtailapi')
# api_router.register_endpoint('comments', CommentAPIViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path("", include("wagtailsurveyjs.urls")),
    path('api/v2/', api_router.urls),

    path('comment/<int:pk>/edit/', views.comment_edit, name='comment_edit'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
    path('api/', include(router.urls)),
    # path('api/comments/<str:post__slug>/', CommentViewSet.as_view({'post': 'list'})),

    # path('visit-count/', views.visits_by_country, name='visits_by_country'),
    path('stats/', views.stats, name='stats'),
]
