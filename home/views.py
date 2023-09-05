from django.shortcuts import render
from .models import HomePage

def home(request):
    home_page = HomePage.objects.first()
    return render(request, "home/home_page.html", {"page": home_page})
