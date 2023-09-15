from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from core.models import Product, Category, Cart, CartItem
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
            product_title = request.POST.get('title')
            product_country = request.POST.get('country')
            quantity = int(request.POST.get('qty'))
            product_price = float(request.POST.get('price'))

            user = request.user

            cart = Cart.objects.get_or_create(user=user)

            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart,
                product_id=product_id,
                defaults={
                    'title': product_title,
                    'country': product_country,
                    'quantity': quantity,
                    'price': product_price
                }
            )

            if not item_created:
                cart_item.quantity += quantity
                cart_item.save()

            return JsonResponse({'message': 'Product added to cart', 'cart_total': cart.total_items})
    except Exception as e:
        return JsonResponse({'error': str(e)})
    
    return JsonResponse({'error': 'Invalid request method'})


def pageNotFound(request, exception):
    return render(request, '404.html')