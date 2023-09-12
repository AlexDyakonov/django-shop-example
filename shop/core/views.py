from django.http import HttpResponse
from django.shortcuts import render

from core.models import Product, Category, CartOrder, CartOrderItems

# Create your views here.

categories = Category.objects.all()

def index(request):
    # products = Product.objects.filter(product_status="published")
    products = Product.objects.all()

    content = {
        'title': 'main',
        "categories" : categories,
        "products" : products,
    }
    return render(request, 'core/index.html', content)

def help(request):
    content = {
        'title': 'Help',
        "categories" : categories,
    }
    return render(request, 'core/help.html', content)

def showcase(request):
    content = {
        'title': 'name',
        "categories" : categories,  
    }
    return render(request, 'core/showcase.html', content)

def item(request):
    content = {
        'title': 'name',
        'itemname': 'category_name',
        "categories" : categories,  
    }
    return render(request, 'core/item.html', content)


def pageNotFound(request, exception):
    return render(request, '404.html')