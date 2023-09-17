from django.contrib import admin
from core.models import Product, Category, Country, Cart, CartItem, Order, Payment

class ProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'category','product_image', 'price', 'product_status']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']

class CountryAdmin(admin.ModelAdmin):
    list_display = ['title']

class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at', 'total_items', 'total_price']

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'country','quantity', 'price', 'total_price', 'cart_item_image']

class OrderAdmin(admin.ModelAdmin):
    list_display = ('oid', 'cart', 'created_at', 'updated_at', 'payment_status')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('oid', 'cart', 'created_at', 'updated_at', 'payment_status')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('title', 'comission')

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)

