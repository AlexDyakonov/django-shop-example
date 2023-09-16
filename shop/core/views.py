from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages

from core.models import Product, Category, Cart, CartItem, Country
import os
from dotenv import load_dotenv

import logging

logger = logging.getLogger(__name__)

load_dotenv()

num_of_products = int(os.getenv("NUMBER_OF_PRODUCTS_ON_MAIN_PAGE"))

# Create your views here.

categories = Category.objects.all()

def index(request):
    # products = Product.objects.filter(product_status="published")
    products = Product.objects.all()

    content = {
        'title': 'CompanyName',
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

def show_category(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(category=category)

    content = {
        'title': category.title,
        "categories": categories,
        "category" : category,  
        "products" : products,
    }
    return render(request, 'core/showcase.html', content)

def show_item(request, pid):
    is_authenticated = request.user.is_authenticated
    item = get_object_or_404(Product, pid=pid)
    products = Product.objects.filter(category=item.category)

    content = {
        'title': item.title,
        'item': item,
        'products': products,
        "categories" : categories,
        'is_authenticated': is_authenticated,
    }
    return render(request, 'core/item.html', content)

@require_POST
def add_to_cart(request):
    try:
        if request.method == 'POST':
            product_id = request.POST.get('id')
            product_country_id = request.POST.get('country')
            quantity = int(request.POST.get('qty'))
            product_price = float(request.POST.get('price'))

            product = Product.objects.get(pk=product_id)
            product_image = product.image

            user = request.user

            cart_tuple = Cart.objects.get_or_create(user=user)
            cart = cart_tuple[0]

            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart,
                product_id=product_id,
                country_id=product_country_id,
                defaults={
                    'image': product_image,
                    'quantity': quantity,
                    'price': product_price
                }
            )
            

            if not item_created:
                cart_item.quantity += quantity
                cart_item.save()

            return JsonResponse({'message': 'Product added to cart', 'cart_total': cart.total_items})
    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e)})
    
    return JsonResponse({'error': 'Invalid request method'})

def show_cart(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Вам необходимо войти в аккаунт.")
        return redirect("core:home")

    cart_tuple = Cart.objects.get_or_create(user=request.user)
    cart = cart_tuple[0]

    cart_items = CartItem.objects.filter(cart = cart)

    content = {
        'title': 'Корзина',
        'categories': categories,
        'cart_items': cart_items,
        'cart': cart,
    }
    return render(request, 'core/cart.html', content)

def pageNotFound(request, exception):
    return render(request, '404.html')