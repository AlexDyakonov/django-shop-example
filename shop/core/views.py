from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def index(request):
    content = {
        'title': 'Hello'
    }
    return render(request, 'core/index.html', content)

def about(request):
    content = {
        'title': 'Hello'
    }
    return render(request, 'core/about.html', content)

def items(request):
    content = {
        'title': 'name',
        'itemname': 'item'        
    }
    return render(request, 'core/items.html', content)

def pageNotFound(request, exception):
    return render(request, 'core/404.html')