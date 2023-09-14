from pyexpat import model
from django import forms
from django.db import models
from shortuuid.django_fields import ShortUUIDField
from userauths.models import User
from django.utils.html import mark_safe

STATUS_CHOICE = {
    ("process", "Processing"),
}

STATUS = {
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("published", "Published"),
}

def user_directiory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="cat", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self) -> str:
        return self.title

class Country(models.Model):
    coid = ShortUUIDField(unique=True, length=10, max_length=30, alphabet="abcdefgh12345")
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self) -> str:
        return self.title
    
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=30, alphabet="abcdefgh12345")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directiory_path, null=False, default="product.png")
    description = models.TextField(null=False, blank=False, default="Товар в нашем магазине")
    specifications = models.TextField(null=False, blank=False, default="Особых свойств нет")

    countries = models.ManyToManyField(Country, related_name='products')

    price = models.DecimalField(max_digits=9, decimal_places=2, default=9.99)

    product_status = models.CharField(choices=STATUS,  max_length=10, default="draft")

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    
    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix= "sku", alphabet="1234567890")

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self) -> str:
        return self.title

# Cart, Order, OrderItem

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=9.99)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=10, default="process")

    class Meta:
        verbose_name_plural = "Cart Order"



class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=9.99)
    total = models.DecimalField(max_digits=9, decimal_places=2, default=9.99)

    class Meta:
        verbose_name_plural = "Cart Order Items"
    
    def order_image(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image.url))

