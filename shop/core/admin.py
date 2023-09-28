from django.contrib import admin
from core.models import Product, Category, Country, Cart, CartItem, Order, Payment
from modeltranslation.admin import TranslationAdmin

class ProductAdmin(TranslationAdmin):
    list_display = ['user', 'title', 'category', 'product_image', 'price', 'product_status']
    prepopulated_fields = {"slug":("title",)}


class CategoryAdmin(TranslationAdmin):
    list_display = ['title']
    prepopulated_fields = {"slug":("title",)}

class CountryAdmin(TranslationAdmin):
    list_display = ['title']

class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at', 'total_items', 'total_price']

class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id','cart', 'product', 'country','quantity', 'price', 'total_price', 'cart_item_image']

class OrderAdmin(admin.ModelAdmin):
    list_display = ('oid', 'cart', 'total', 'created_at', 'updated_at', 'payment_status')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'order', 'description', 'created_at')


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Payment, PaymentAdmin)