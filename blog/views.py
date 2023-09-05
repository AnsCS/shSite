from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView
from wagtail.models import Page

from .models import Comment
from django.http import HttpResponse

from django.views.decorators.cache import cache_page

from wagtail.views import serve

def cached_serve(request, path):
    return cache_page(60 * 15)(serve)(request, path)
from wagtail.search.models import Query

def search(request):
    search_query = request.GET.get('query', None)
    page = request.GET.get('page', 1)

    # Perform primary search on title field
    search_results = Page.objects.live().search(search_query, fields=['title'])

    # Perform secondary search on intro field if no results are found
    if not search_results:
        search_results = Page.objects.live().search(search_query, fields=['intro'])

    # Record the query so Wagtail can suggest promoted results
    Query.get(search_query).add_hit()

    return render(request, 'search/search.html', {
        'search_query': search_query,
        'search_results': search_results,
    })




def comment_edit(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        comment.name = request.POST.get('name')
        comment.email = request.POST.get('email')
        comment.body = request.POST.get('body')
        comment.save()
        return redirect(comment.post.url)
    else:
        return render(request, 'comment_edit.html', {'comment': comment})


def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_url = comment.post.url
    comment.delete()
    return redirect(post_url)



# class SearchView(TemplateView):
#     template_name = 'search_results.html'

#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     query = self.request.GET.get('query')
#     #     if query:
#     #         results = Page.objects.live().search(query)
#     #         context['results'] = results
#     #     return context
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         query = self.request.GET.get('query')
#         if query:
#             # Search in titles first
#             results = Page.objects.live().search(query, fields=['title'])
#             # If no results found, search in body
#             if not results:
#                 results = Page.objects.live().search(query, fields=['intro'])
#             context['results'] = results
#         return context


# from rest_framework import viewsets, serializers
# from .models import BlogCategory

# class BlogCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BlogCategory
#         fields = ['name', 'icon']

# class BlogCategoryViewSet(viewsets.ModelViewSet):
#     queryset = BlogCategory.objects.all()
#     serializer_class = BlogCategorySerializer


from rest_framework import viewsets, serializers
from rest_framework.pagination import LimitOffsetPagination
from blog.models import BlogPage, BlogCategory, Comment

class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategory
        fields = ['id', 'name', 'icon']

class BlogPageSerializer(serializers.ModelSerializer):
    categories = BlogCategorySerializer(many=True, read_only=True)
    featured_image_url = serializers.SerializerMethodField()

    class Meta:
        model = BlogPage
        fields = ['search_image','slug', 'id', 'title', 'intro', 'date', 'summary', 'featured_image_url', 'categories']

    def get_featured_image_url(self, obj):
        if obj.featured_image:
            return obj.featured_image.file.url
        return None


class BlogCategoryViewSet(viewsets.ModelViewSet):
    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer

class BlogPageViewSet(viewsets.ModelViewSet):
    queryset = BlogPage.objects.all()
    serializer_class = BlogPageSerializer

# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = ['id', 'post__slug', 'name', 'email', 'body', 'created_at']

# class CommentViewSet(viewsets.ModelViewSet):
#     serializer_class = CommentSerializer
#     lookup_field = 'post__slug'
#     lookup_url_kwarg = 'slug'

#     def get_queryset(self):
#         queryset = Comment.objects.all()
#         slug = self.kwargs.get(self.lookup_url_kwarg)
#         if slug is not None:
#             post = get_object_or_404(BlogPage, slug=slug)
#             queryset = queryset.filter(post=post)
#         return queryset


# class CommentSerializer(serializers.ModelSerializer):
#     post_title = serializers.SerializerMethodField()
#     post_slug = serializers.SerializerMethodField()

#     class Meta:
#         model = Comment
#         fields = ['id', 'post', 'post_title', 'post_slug', 'name', 'body', 'created_at']

#     def get_post_title(self, obj):
#         return obj.post.title

#     def get_post_slug(self, obj):
#         return obj.post.slug

# class CommentViewSet(viewsets.ModelViewSet):
#     serializer_class = CommentSerializer
#     lookup_field = 'post__slug'
#     lookup_url_kwarg = 'slug'

#     def get_queryset(self):
#         queryset = Comment.objects.all()
#         slug = self.kwargs.get(self.lookup_url_kwarg)
#         if slug is not None:
#             post = get_object_or_404(BlogPage, slug=slug)
#             queryset = queryset.filter(post=post)
#         return queryset


from wagtail.api.v2.views import BaseAPIViewSet
from .serializers import CommentSerializer
class CommentAPIViewSet(BaseAPIViewSet):
    model = Comment
    api_fields = ['name', 'body']
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        slug = self.request.query_params.get('slug')
        if slug is not None:
            post = get_object_or_404(BlogPage, slug=slug)
            queryset = queryset.filter(post=post)
        return queryset


# class CommentViewSet(viewsets.ModelViewSet):
#     serializer_class = CommentSerializer
#     pagination_class = LimitOffsetPagination
#     max_limit = 10

#     def get_queryset(self):
#         queryset = Comment.objects.all()
#         post_slug = self.kwargs.get('post_slug', None)
#         if post_slug is not None:
#             queryset = queryset.filter(post_slug=post_slug).values()
#         return queryset


# from django.shortcuts import render
# from django.utils import timezone
# from .models import SiteVisitCount, SiteVisit

# def visit_count(request):
#     visit_count = SiteVisitCount.objects.first().visit_count

#     today = timezone.now().date()
#     week_ago = today - timezone.timedelta(weeks=1)
#     month_ago = today - timezone.timedelta(days=30)

#     daily_visits = SiteVisit.objects.filter(date=today).count()
#     weekly_visits = SiteVisit.objects.filter(date__gte=week_ago).count()
#     monthly_visits = SiteVisit.objects.filter(date__gte=month_ago).count()

#     context = {
#         'visit_count': visit_count,
#         'daily_visits': daily_visits,
#         'weekly_visits': weekly_visits,
#         'monthly_visits': monthly_visits,
#     }

#     return render(request, 'visit_count.html', context)

from django.db.models import Count
# from .models import SiteVisit

# def visits_by_country(request):
#     visits = SiteVisit.objects.values('country').annotate(count=Count('country')).order_by('-count')
#     return render(request, 'visit_count.html', {'visits': visits})


from django.shortcuts import render
from django.utils import timezone
from calendar import monthrange
from .models import IpAddress

from calendar import month_name

from django.shortcuts import render
from django.utils import timezone
from calendar import monthrange, month_name
from .models import IpAddress
from django.utils import timezone
from calendar import monthrange, month_name
from calendar import month_name

from django.shortcuts import render
from django.utils import timezone
from calendar import monthrange, month_name
from .models import IpAddress

from calendar import month_name

from django.shortcuts import render
from django.utils import timezone
from calendar import monthrange, month_name
from .models import IpAddress

def track_visit(ip_address, country):
    # الحصول على تاريخ اليوم
    today = timezone.now().date()

    # البحث عن سجل IpAddress لعنوان IP معين
    ip_address_obj = IpAddress.objects.filter(ip_address=ip_address).first()

    if ip_address_obj:
        if ip_address_obj.last_visit.month != today.month or ip_address_obj.last_visit.year != today.year:
            # زيارة جديدة في شهر جديد
            IpAddress.objects.create(ip_address=ip_address, country=country)
        else:
            # تحديث تاريخ الزيارة الأخيرة
            ip_address_obj.last_visit = today
            ip_address_obj.save()
    else:
        # إنشاء سجل جديد
        IpAddress.objects.create(ip_address=ip_address, country=country)
import datetime

from django.contrib import messages

from django.db.models.functions import ExtractHour
from django.db.models import Case, When, Value, F
from blog.models import BlogPage
from django.db.models import Subquery, OuterRef, Count
from blog.models import BlogPage, Comment

def stats(request):
    context = {}

    # التحقق مما إذا كان المستخدم قد حدد شهرًا وسنة
    month = request.GET.get('month')
    year = request.GET.get('year')

    # الحصول على تاريخ اليوم
    today = timezone.now().date()

    # حساب عدد الزيارات لكل يوم في الشهر المحدد
    monthly_visits = []
    if month:
        days_in_month = monthrange(today.year, int(month))[1]
        for day in range(1, days_in_month + 1):
            date = today.replace(day=day, month=int(month))
            visits = IpAddress.objects.filter(created_at__date=date).count()
            monthly_visits.append({'date': date, 'visits': visits})
        context['monthly_visits'] = monthly_visits

        # حساب عدد الزيارات الكلية للشهر المحدد
        total_monthly_visits = IpAddress.objects.filter(created_at__month=month, created_at__year=today.year).count()
        context['total_monthly_visits'] = total_monthly_visits

    # حساب عدد الزيارات لكل دولة
    if month:
        country_visits = IpAddress.objects.filter(created_at__month=month, created_at__year=today.year).values('country').annotate(visits=Count('country')).order_by('-visits')

        if not country_visits:
            messages.warning(request, 'لا توجد بيانات في قاعدة البيانات للشهر والسنة المحددين.')
    else:
        country_visits = IpAddress.objects.values('country').annotate(visits=Count('country')).order_by('-visits')
    context['country_visits'] = country_visits


    hourly_visits = IpAddress.objects.filter(created_at__month=month, created_at__year=today.year).annotate(hour=ExtractHour('created_at')).annotate(hour_12=F('hour') % 12).annotate(period=Case(When(hour__lt=12, then=Value('AM')), When(hour__gte=12, then=Value('PM')))).values('hour_12', 'period').annotate(visits=Count('id')).order_by('hour')
    context['hourly_visits'] = hourly_visits

    def get_years():
        # الحصول على قائمة بجميع السنوات المختلفة
        years = IpAddress.objects.dates('created_at', 'year').values_list('created_at__year', flat=True).distinct()
        return years

    # الحصول على قائمة بجميع السنوات المختلفة
    years = get_years()
    context['years'] = years

    # إعداد بيانات الرسم البياني
    chart_labels = []
    chart_data = []
    if monthly_visits:
        for visit in monthly_visits:
            chart_labels.append(visit['date'].strftime('%d %b'))
            chart_data.append(visit['visits'])

    # تمرير بيانات الرسم البياني إلى القالب
    context['chart_labels'] = chart_labels
    context['chart_data'] = chart_data


    # إعداد بيانات الرسم البياني
    country_labels = []
    country_data = []
    if country_visits:
        for visit in country_visits:
            country_labels.append(visit['country'])
            country_data.append(visit['visits'])

    # تمرير بيانات الرسم البياني إلى القالب
    context['country_labels'] = country_labels
    context['country_data'] = country_data

    # Query all the blog pages with their view counts and urls
    blog_pages = BlogPage.objects.order_by('-view_count')
    blog_views = [{'title': page.title, 'view_count': page.view_count, 'url': page.get_url()} for page in blog_pages]
    context['blog_views'] = blog_views

    # Query all the blog pages with their view counts, urls, and comment counts
    comment_count_subquery = Subquery(Comment.objects.filter(post=OuterRef('pk')).values('post').annotate(count=Count('pk')).values('count'))
    blog_pages = BlogPage.objects.annotate(comment_count=comment_count_subquery).order_by('-view_count')
    blog_views = [{'title': page.title, 'view_count': page.view_count, 'url': page.get_url(), 'comment_count': page.comment_count} for page in blog_pages]
    context['blog_views'] = blog_views

    return render(request, 'stats.html', context)


# def save_visit(request):
#     if request.method == 'POST':
#         ip = request.META.get('REMOTE_ADDR')
#         url = request.POST.get('url')
#         time_spent = request.POST.get('timeSpent')
#         visit_ip, created = VisitIp.objects.get_or_create(ip=ip, url=url)
#         visit_ip.time_spent = time_spent
#         visit_ip.save()
#         return JsonResponse({'status': 'success'})
#     else:
#         return JsonResponse({'status': 'error'})

from django.http import JsonResponse

# def save_time(request):
#     if request.method == 'POST':
#         time_spent = request.POST.get('timeSpent')
#         request.session['time_spent'] = time_spent
#         return JsonResponse({'status': 'success'})
#     else:
#         return JsonResponse({'status': 'error'})

# from rest_framework import viewsets
# from .models import VisitIp
# from .serializers import VisitIpSerializer

# class VisitIpViewSet(viewsets.ModelViewSet):
#     queryset = VisitIp.objects.all()
#     serializer_class = VisitIpSerializer

# from django.shortcuts import render
# from .models import VisitIp

# def show_visits(request):
#     visits = VisitIp.objects.all()
#     return render(request, 'show_visits.html', {'visits': visits})

# from datetime import timedelta
# from django.http import JsonResponse
# from .models import VisitIp

# def update_time_spent(request):
#     # الحصول على عنوان IP الخارجي للمستخدم
#     ip_address = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_X_FORWARDED_FOR')
#     if not ip_address:
#         ip_address = request.META.get('REMOTE_ADDR')

#     # الحصول على عنوان URL للصفحة التي يزورها المستخدم
#     url = request.build_absolute_uri()

#     # البحث عن سجل في قاعدة البيانات يطابق عنوان IP وعنوان URL
#     visit_ip_obj = VisitIp.objects.filter(ip=ip_address, url=url).first()

#     if visit_ip_obj:
#         # إذا تم العثور على سجل، قم بتحديث المدة الزمنية التي يقضيها المستخدم على الصفحة
#         visit_ip_obj.time_spent += timedelta(seconds=3)
#         visit_ip_obj.save()

#     return JsonResponse({'success': True})


# from django.db.models import Avg
# from django.shortcuts import render
# from .models import VisitIp
# from django.contrib.admin.views.decorators import staff_member_required

# @staff_member_required
# def visit_ip_list(request):
#     visit_ips = VisitIp.objects.exclude(url__contains='/visit-ip-list/').exclude(url__contains='/stats/').exclude(url__contains='/media/images/')
#     url_averages = VisitIp.objects.values('url').annotate(avg_time_spent=Avg('time_spent'))

#     return render(request, 'visit_ip_list.html', {'visit_ips': visit_ips, 'url_averages': url_averages})






# from django.shortcuts import render
# from .models import VisitIp

# def visit_stats(request):
#     visits = VisitIp.objects.all()
#     return render(request, 'visit_stats.html', {'visits': visits})


# from django.shortcuts import render
# from .models import VisitIp

# def track_user(request):
#     if request.method == 'POST':
#         ip_address = request.META.get('REMOTE_ADDR')
#         url = request.POST.get('url')
#         time_spent = request.POST.get('time_spent')
#         VisitIp.objects.create(ip=ip_address, url=url, time_spent=time_spent)
#     data = VisitIp.objects.all()
#     return render(request, 'results.html', {'data': data})

# from django.shortcuts import render
# from .models import UserTracking

# def display_results(request):
#     data = UserTracking.objects.all()
#     return render(request, 'results.html', {'data': data})


# def calculate_time_spent(request):
#     start_time = request.session.get('start_time')
#     if start_time:
#         start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
#         time_spent = datetime.now() - start_time
#         request.session['start_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         return time_spent
#     else:
#         request.session['start_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         return timedelta(0)




# from django.contrib.sessions.models import Session
# from .models import BlogPage

# def my_view(request):
#     print('my_view called')
#     session = Session.objects.get(session_key=request.session.session_key)
#     page = BlogPage.objects.get(title='ni')
#     visit_session = VisitSession(
#         session=session,
#         page=page,
#         device_type=request.META['HTTP_USER_AGENT'],
#         time_spent=calculate_time_spent(request),
#         url=request.build_absolute_uri()
#     )
#     visit_session.save()
#     return render(request, 'my_template.html', {'my_context': 'value'})



# from django.http import JsonResponse
# from django.utils import timezone
# from .models import PageVisit

# def record_page_visit(request):
#     if request.method == 'POST':
#         session = request.session
#         device_type = request.POST.get('device_type')
#         start_time = timezone.datetime.fromtimestamp(int(request.POST.get('start_time')))
#         end_time = timezone.datetime.fromtimestamp(int(request.POST.get('end_time')))
#         time_spent = end_time - start_time
#         url = request.POST.get('url')

#         page_visit = PageVisit.objects.create(session=session, device_type=device_type, time_spent=time_spent, url=url)

#         return JsonResponse({'status': 'success'})

#     return JsonResponse({'status': 'error'})


# from django.db.models import Avg
# from .models import PageVisit

# from django.shortcuts import render
# from .models import PageVisit

# def stats_session(request):
#     context = {}

#     # Query all page visits
#     page_visits = PageVisit.objects.all()
#     context['page_visits'] = page_visits

#     return render(request, 'stats_session.html', context)


##################### old code ###########
# def stats(request):

#     context = {}


#     # التحقق مما إذا كان المستخدم قد حدد شهرًا وسنة
#     month = request.GET.get('month')
#     year = request.GET.get('year')

#     # الحصول على تاريخ اليوم
#     today = timezone.now().date()

#     # حساب عدد الزيارات لكل يوم في الشهر المحدد
#     monthly_visits = []
#     if month:
#         days_in_month = monthrange(today.year, int(month))[1]
#         for day in range(1, days_in_month + 1):
#             date = today.replace(day=day, month=int(month))
#             visits = IpAddress.objects.filter(created_at__date=date).count()
#             monthly_visits.append({'date': date, 'visits': visits})
#         context['monthly_visits'] = monthly_visits

#         # حساب عدد الزيارات الكلية للشهر المحدد
#         total_monthly_visits = IpAddress.objects.filter(created_at__month=month, created_at__year=today.year).count()
#         context['total_monthly_visits'] = total_monthly_visits

#     # حساب عدد الزيارات لكل دولة
#     # country_visits = IpAddress.objects.values('country').annotate(visits=Count('country')).order_by('-visits')
#     # context['country_visits'] = country_visits

#     if month:
#         country_visits = IpAddress.objects.filter(created_at__month=month, created_at__year=today.year).values('country').annotate(visits=Count('country')).order_by('-visits')

#         if not country_visits:
#             messages.warning(request, 'لا توجد بيانات في قاعدة البيانات للشهر والسنة المحددين.')
#     else:
#         country_visits = IpAddress.objects.values('country').annotate(visits=Count('country')).order_by('-visits')
#     context['country_visits'] = country_visits



#     # حساب عدد الزيارات لكل دولة
#     # if month:
#     #     country_visits = IpAddress.objects.filter(created_at__month=month, created_at__year=today.year).values('country').annotate(visits=Count('country')).order_by('-visits')
#     # else:
#     #     country_visits = IpAddress.objects.values('country').annotate(visits=Count('country')).order_by('-visits')
#     # context['country_visits'] = country_visits

#     def get_years():
#         # الحصول على قائمة بجميع السنوات المختلفة
#         years = IpAddress.objects.dates('created_at', 'year').values_list('created_at__year', flat=True).distinct()
#         return years


#     # الحصول على قائمة بجميع السنوات المختلفة
#     years = get_years()
#     context['years'] = years

#       # إعداد بيانات الرسم البياني
#     chart_labels = []
#     chart_data = []
#     if monthly_visits:
#         for visit in monthly_visits:
#             chart_labels.append(visit['date'].strftime('%d %b'))
#             chart_data.append(visit['visits'])

#     # تمرير بيانات الرسم البياني إلى القالب
#     context['chart_labels'] = chart_labels
#     context['chart_data'] = chart_data

#     # إعداد بيانات الرسم البياني
#     country_labels = []
#     country_data = []
#     if country_visits:
#         for visit in country_visits:
#             country_labels.append(visit['country'])
#             country_data.append(visit['visits'])

#     # تمرير بيانات الرسم البياني إلى القالب
#     context['country_labels'] = country_labels
#     context['country_data'] = country_data


#     return render(request, 'stats.html', context)

########################################################## old

