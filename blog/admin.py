from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import IpAddress

@admin.register(IpAddress)
class IpAddressAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'country', 'city' ,'created_at')


from .models import BlogPage

class BlogPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'view_count')

# class CommentAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'created_at')

# class VisitSessionAdmin(admin.ModelAdmin):
#     list_display = ('session', 'device_type', 'time_spent', 'url')

admin.site.register(BlogPage, BlogPageAdmin)
# admin.site.register(Comment, CommentAdmin)
# admin.site.register(PageVisit, PageVisitAdmin)
