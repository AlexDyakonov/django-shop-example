from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from coinbase_commerce.client import Client
from core.tasks import delete_payment
from coinbase_commerce.error import SignatureVerificationError, WebhookInvalidPayload
from coinbase_commerce.webhook import Webhook
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from django.utils.translation import gettext as _
from django.utils.translation import get_language

from core.models import Product, Category, Cart, CartItem, Payment, Order

from email_utils.email_utils import send_order_confirmation_email, send_create_order_mail, send_cancel_order_mail

import os
from dotenv import load_dotenv

load_dotenv()

num_of_products = int(os.getenv("NUMBER_OF_PRODUCTS_ON_MAIN_PAGE"))

def exit_if_not_logged_in(request):
    if not request.user.is_authenticated:
        messages.warning(request, _("Вам необходимо войти в аккаунт."))
        return True
    return False

from django.utils.translation import get_language


messages_locale = {
    'en': {
        "help_title": "Support",
        "cart_title": "Cart",
        "checkout_title": "Order",
        "success_title": "Success",
        "cancel_title": "Cancel",
        "order_on_site" : "Payment on site ",
        "order": "Order ",
    },
    'ru': {
        "help_title": "Поддержка",
        "cart_title": "Корзина",
        "checkout_title": "Оформление заказа",
        "success_title": "Успешно",
        "cancel_title": "Отмена",
        "order_on_site" : "Оплата заказа на сайте ",
        "order": "Заказ ",
    },
}

def get_message(msg_id):
    current_language = get_language()
    if current_language in messages_locale:
        if msg_id in messages_locale[current_language]:
            return messages_locale[current_language][msg_id]
    
    return "None"


categories = Category.objects.all()

def index(request):
    products = Product.objects.filter(product_status="published")

    content = {
        'title': os.getenv("SITE_NAME"),
        "categories" : categories,
        "products" : products,
    }

    filtered_products = {}
    for category in categories:
        category_products = products.filter(category=category, product_status="published")[:num_of_products]  
        filtered_products[category] = category_products

    content['filtered_products'] = filtered_products

    return render(request, 'core/index.html', content)

def help(request):
    content = {
        'title': get_message("help_title"),
        "categories" : categories,
    }
    return render(request, 'core/help.html', content)

def show_category(request, cat_slug): 
    category = get_object_or_404(Category, slug=cat_slug)
    products = Product.objects.filter(category=category)

    content = {
        'title': category.title,
        "categories": categories,
        "category" : category,  
        "products" : products,
    }
    return render(request, 'core/showcase.html', content)

def show_item(request, item_slug):
    is_authenticated = request.user.is_authenticated
    item = get_object_or_404(Product, slug=item_slug)
    products = Product.objects.filter(category=item.category, product_status="published")

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
    if exit_if_not_logged_in(request):
        return redirect("core:home")
    
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
    if exit_if_not_logged_in(request):
        return redirect("core:home")
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
    if exit_if_not_logged_in(request):
        return redirect("core:home")
    
    is_authenticated = request.user.is_authenticated
    
    cart_tuple = Cart.objects.get_or_create(user=request.user)
    cart = cart_tuple[0]

    cart_items = CartItem.objects.filter(cart = cart)
    cart_items_exist = cart_items.exists

    content = {
        'title': get_message("cart_title"),
        'categories': categories,
        'cart_items': cart_items,
        'cart': cart,
        'is_authenticated': is_authenticated,
        'cart_items_exist': cart_items_exist,
    }
    return render(request, 'core/cart.html', content)

def update_cart_item(request):
    if exit_if_not_logged_in(request):
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
    
def create_order(request):
    if exit_if_not_logged_in(request):
        return redirect("core:home")

    if request.method == 'POST':
        user = request.user

        cart, created = Cart.objects.get_or_create(user=user)

        order = Order.objects.get_or_create(cart=cart, payment_status = 'pending')
        
        order[0].total = cart.total_price()
        order[0].save()      

        return redirect('core:checkout')

    return redirect('core:cart')

def show_checkout(request):
    if exit_if_not_logged_in(request):
        return redirect("core:home")
    
    cart_tuple = Cart.objects.get_or_create(user=request.user)
    cart = cart_tuple[0]

    cart_items = CartItem.objects.filter(cart = cart)
    cart_items_exist = cart_items.exists

    content = {
        'title': get_message("checkout_title"),
        'categories': categories,
        'user': request.user,
        'cart_items': cart_items,
        'cart_items_exist': cart_items_exist,
        'is_authenticated': request.user.is_authenticated,
        'cart': cart,
    }
    return render(request, 'core/checkout.html', content)

def success_view(request):
    if exit_if_not_logged_in(request):
        return redirect("core:home")
    content = {
        'title': get_message("success_title"),
        'categories': categories,
    }
    return render(request, 'core/success.html', content)


def cancel_view(request):
    if exit_if_not_logged_in(request):
        return redirect("core:home")
    content = {
        'title': get_message("cancel_title"),
        'categories': categories,
    }
    return render(request, 'core/cancel.html', content)


def create_payment(request):
    if exit_if_not_logged_in(request):
        return redirect("core:home")
    
    if request.method == 'POST':
        api_key = settings.COINBASE_API_KEY

        user = request.user
        cart = get_object_or_404(Cart, user=user)
        order_tuple = Order.objects.get_or_create(Order, cart=cart, payment_status='pending')
        order = order_tuple[0]

        total = cart.total_price()

        payment = Payment.objects.get_or_create(order=order, description=user.email)

        order_string = get_message("order")

        client = Client(api_key)
        charge_data = {
            "name": order_string + "#" + str(order.oid).replace("order", ""), 
            "description": get_message("order_on_site") + os.getenv("SITE_NAME"),
            "local_price": {
                "amount": float(total),
                "currency": "USD"  
            },
            "pricing_type": "fixed_price", 
            'redirect_url': request.build_absolute_uri(reverse('core:payments-success')),
            'cancel_url': request.build_absolute_uri(reverse('core:payments-cancel')),
            'metadata': {
                "order_id": order.pk,
                "user_mail": request.user.email,
                "order_name": str(order.oid).replace("order", ""),
                "language": get_language(),
            }
        }   

        charge = client.charge.create(**charge_data)

        return redirect(charge.hosted_url)

    return redirect("core:cart")

@ensure_csrf_cookie
@csrf_exempt
@require_http_methods(['POST'])
def coinbase_webhook(request):
    request_data = request.body.decode('utf-8')
    request_sig = request.headers.get('X-CC-Webhook-Signature', None)
    webhook_secret = settings.COINBASE_WEBHOOK_SECRET

    try:
        event = Webhook.construct_event(request_data, request_sig, webhook_secret)

        # https://commerce.coinbase.com/docs/api/#webhooks

        if event['type'] == 'charge:created':
            order_id = event['data']['metadata']['order_id']
            payment_url = event['data']['hosted_url']
            language = event['data']['metadata']['language']

            order = Order.objects.get(pk=order_id)
            send_create_order_mail(user=order.cart.user, order_id=str(order.oid).replace("order", ""), order_amount=order.total, payment_link=payment_url, language = language)

        if event['type'] == 'charge:failed':
            order_id = event['data']['metadata']['order_id']
            language = event['data']['metadata']['language']

            order = Order.objects.get(pk=order_id)
            order.payment_status = 'failed'
            order.save()

            send_cancel_order_mail(user=order.cart.user, order_id=str(order.oid).replace("order", ""), language = language)

        if event['type'] == 'charge:confirmed':
            order_id = event['data']['metadata']['order_id']
            language = event['data']['metadata']['language']

            order = Order.objects.get(pk=order_id)
            order.payment_status = 'paid'
            order.save()

            CartItem.objects.filter(cart=order.cart).get().delete()
            send_order_confirmation_email(user=order.cart.user, order_id=str(order.oid).replace("order", ""), amount=order.total, order_date=order.created_at, language = language)
            

    except (SignatureVerificationError, WebhookInvalidPayload) as e:
        return HttpResponse(e, status=400)


    return HttpResponse('ok', status=200)

def pageNotFound(request, exception):
    return render(request, '404.html')