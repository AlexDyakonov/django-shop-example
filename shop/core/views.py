from django.http import HttpResponse
from django.shortcuts import render

from core.models import Product, Category, CartOrder, CartOrderItems
import os
from dotenv import load_dotenv

load_dotenv()

num_of_products = int(os.getenv("NUMBER_OF_PRODUCTS_ON_MAIN_PAGE"))

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

    filtered_products = {}
    for category in categories:
        category_products = products.filter(category=category)[:num_of_products]  
        filtered_products[category] = category_products

    content['filtered_products'] = filtered_products

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