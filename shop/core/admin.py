from django.contrib import admin
from core.models import Product, Category, Country, CartOrder, CartOrderItems

class ProductAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'category','product_image', 'price', 'product_status']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title']

class CountryAdmin(admin.ModelAdmin):
    list_display = ['title']

class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'price', 'paid_status', 'order_date', 'product_status']

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item', 'image', 'quantity', 'price', 'total']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)