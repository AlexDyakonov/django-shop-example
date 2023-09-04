from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def index(request):
    content = {
        'title': 'Hello'
    }
    return render(request, 'core/index.html', content)

def main(request):
    content = {
        'title': 'Hello'
    }
    return render(request, 'core/main.html', content)

def about(request):
    content = {
        'title': 'Hello'
    }
    return render(request, 'core/about.html', content)


def pageNotFound(request, exception):
    return render(request, 'core/404.html')