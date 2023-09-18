from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from coinbase_commerce.client import Client

from core.models import Product, Category, Cart, CartItem, Payment
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

@require_POST
def remove_from_cart(request):
    try:
        if request.method == 'POST':
            product_id = request.POST.get('id')
            user = request.user

            cart_tuple = Cart.objects.get_or_create(user=user)
            cart = cart_tuple[0]

            cart_item = CartItem.objects.get(cart=cart.id, id=product_id)
            cart_item.delete()

            cart_items = CartItem.objects.filter(cart = cart.id)

            if cart_items.exists:
                new_cart_total_price = cart.total_price()
                return JsonResponse({'message': 'Product removed from cart', 'cart_total_price': new_cart_total_price})
            else:
                return JsonResponse({'message': 'Product removed from cart', 'cart_is_empty': True})
            
    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e)})
    
    return JsonResponse({'error': 'Invalid request method'})

def show_cart(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Вам необходимо войти в аккаунт.")
        return redirect("core:home")
    is_authenticated = request.user.is_authenticated
    
    cart_tuple = Cart.objects.get_or_create(user=request.user)
    cart = cart_tuple[0]

    cart_items = CartItem.objects.filter(cart = cart)
    cart_items_exist = cart_items.exists

    content = {
        'title': 'Корзина',
        'categories': categories,
        'cart_items': cart_items,
        'cart': cart,
        'is_authenticated': is_authenticated,
        'cart_items_exist': cart_items_exist,
    }
    return render(request, 'core/cart.html', content)

def update_cart_item(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Вам необходимо войти в аккаунт.")
        return redirect("core:home")
    
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        quantity = request.POST.get('quantity')

        cart = Cart.objects.get_or_create(user=request.user)
        
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart=cart[0])
        
        cart_item.quantity = int(quantity)
        cart_item.save()
        
        item_cart_total_price = cart_item.total_price()
        new_cart_total_price = cart[0].total_price()

        return JsonResponse({'success': True, 'item_cart_total_price': item_cart_total_price, 'cart_total_price': new_cart_total_price})
    else:
        return JsonResponse({'success': False})

def show_checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Вам необходимо войти в аккаунт.")
        return redirect("core:home")
    
    cart_tuple = Cart.objects.get_or_create(user=request.user)
    cart = cart_tuple[0]

    cart_items = CartItem.objects.filter(cart = cart)
    cart_items_exist = cart_items.exists

    content = {
        'title': 'Оформление заказа',
        'categories': categories,
        'user': request.user,
        'cart_items': cart_items,
        'cart_items_exist': cart_items_exist,
        'cart': cart,
    }
    return render(request, 'core/checkout.html', content)

def create_payment(request):
    if request.method == 'POST':
        # Прописать получение данных о заказе

        client = Client(api_key=settings.COINBASE_API_KEY)
        charge_data = {
            'name': 'Order Payment',
            'description': 'Payment for an order',
            'local_price': {
                'amount': '10.00',  
                'currency': 'USD',
            },
            'pricing_type': 'fixed_price',
            'metadata': {
                'order_id': '12345',  
            },
        }
        charge = client.charge.create(**charge_data)

        Payment.objects.create(charge_id=charge.id, description=charge.description, amount=charge.local_price.amount)

        payment_url = charge.hosted_url

        return render(request, 'payments/payment_page.html', {'payment_url': payment_url})

    return render(request, 'core/checkout.html')

def pageNotFound(request, exception):
    return render(request, '404.html')