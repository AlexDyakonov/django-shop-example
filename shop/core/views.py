from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def index(request):
    content = {
        'title': 'Hello'
    }
    return render(request, 'core/index.html', content)

def help(request):
    content = {
        'title': 'Help'
    }
    return render(request, 'core/help.html', content)

def showcase(request):
    content = {
        'title': 'name',
        'itemname': 'category_name'        
    }
    return render(request, 'core/showcase.html', content)

def item(request):
    content = {
        'title': 'name',
        'itemname': 'category_name'        
    }
    return render(request, 'core/item.html', content)


def pageNotFound(request, exception):
    return render(request, 'core/404.html')