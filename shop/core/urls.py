from django.urls import path, re_path
from core.views import index, help, show_category, show_item, show_cart, add_to_cart

app_name = "core"

urlpatterns = [
    path('', index, name='home'),
    path('help/', help, name='help'),
    
    path('category/<str:cid>/', show_category, name='category'),
    path('item/<str:pid>/', show_item, name='item'),

    path('cart/', show_cart, name="cart"),
    path('add-to-cart', add_to_cart, name="add-to-cart"),
]