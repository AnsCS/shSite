import csv
from datetime import datetime

# def save_visitor_ip(request):
#     ip = request.META.get('REMOTE_ADDR')
#     date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     url = request.path
#     with open('visitors.csv', 'a') as file:
#         writer = csv.writer(file)
#         writer.writerow([ip, date, url])

# class SaveVisitorIPMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if not request.path.startswith('/admin') and request.path != '/favicon.ico':
#             save_visitor_ip(request)
#         response = self.get_response(request)
#         return response

import requests
from datetime import datetime
from django.utils.deprecation import MiddlewareMixin
from .models import IpAddress


import requests
from requests.exceptions import ConnectionError
from datetime import datetime
from django.utils.deprecation import MiddlewareMixin
from .models import IpAddress

class SaveIpAddressMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # الحصول على تاريخ اليوم
        today = datetime.now().date()

        # البحث عن عنوان IP الحقيقي للمستخدم في رؤوس الطلب
        ip_address = request.META.get('HTTP_X_REAL_IP') or request.META.get('HTTP_X_FORWARDED_FOR')

        # إذا لم يتم العثور على عنوان IP في رؤوس الطلب، استخدم عنوان IP المحلي
        if not ip_address:
            ip_address = request.META.get('REMOTE_ADDR')

        # استخدام خدمة تحديد الموقع للحصول على اسم الدولة واسم المدينة من عنوان IP
        try:
            response = requests.get(f'http://ip-api.com/json/{ip_address}')
            data = response.json()
            country = data.get('country', '')
            city = data.get('city', '')
        except ConnectionError:
            # التعامل مع حالات فشل الاتصال
            country = ''
            city = ''

        # التحقق من وجود عنوان IP في قاعدة البيانات قبل حفظه
        ip_address_obj = IpAddress.objects.filter(ip_address=ip_address, created_at__year=today.year, created_at__month=today.month).first()

        if not ip_address_obj:
            # إنشاء سجل جديد
            IpAddress.objects.create(ip_address=ip_address, country=country, city=city)
