from django.urls import path, re_path
from core.views import index, help, show_category, show_item, show_cart, add_to_cart, remove_from_cart, update_cart_item, show_checkout

app_name = "core"

urlpatterns = [
    path('', index, name='home'),
    path('help/', help, name='help'),
    
    path('category/<str:cid>/', show_category, name='category'),
    path('item/<str:pid>/', show_item, name='item'),

    path('cart/', show_cart, name="cart"),
    path('add-to-cart', add_to_cart, name="add-to-cart"),
    path('remove-from-cart', remove_from_cart, name="remove-from-cart"),
    path('update-cart-item', update_cart_item, name="update-cart-item"),

    path('checkout/', show_checkout, name="checkout"),

]