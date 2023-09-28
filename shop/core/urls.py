from django.urls import path, re_path
from core.views import index, help, show_category, show_item, show_cart, add_to_cart, remove_from_cart, update_cart_item, show_checkout, create_payment, create_order, success_view, cancel_view, coinbase_webhook

app_name = "core"

urlpatterns = [
    path('', index, name='home'),
    path('help/', help, name='help'),
    
    path('category/<slug:cat_slug>/', show_category, name='category'),
    path('item/<slug:item_slug>/', show_item, name='item'),

    path('cart/', show_cart, name="cart"),
    path('create-order/', create_order, name='create-order'),
    path('checkout/', show_checkout, name="checkout"),

    path('success/', success_view, name='payments-success'),
    path('cancel/', cancel_view, name='payments-cancel'),
]