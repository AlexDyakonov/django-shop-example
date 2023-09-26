from pyexpat import model
from django import forms
from django.db import models
from shortuuid.django_fields import ShortUUIDField
from userauths.models import User
from django.utils.html import mark_safe
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator 

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

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_items(self):
        return self.cartitem_set.count()

    def total_price(self):
        return sum(item.total_price() for item in self.cartitem_set.all())

    def __str__(self):
        return f"Cart for {self.user.username}"
    
    class Meta:
        verbose_name_plural = "Carts"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, default="1")
    image = models.ImageField(upload_to=user_directiory_path, null=False, default="product.png")    
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2) 

    def clean(self):
        super().clean()
        if self.quantity < 1:  
            self.quantity = 1  

    def cart_item_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product.title} ({self.quantity} units)"
    
    class Meta:
        verbose_name_plural = "Cart items"

class Order(models.Model):
    oid = ShortUUIDField(unique=True, length=10, max_length=30, prefix="order", alphabet="abcdefgh12345")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Ожидание оплаты'),
        ('paid', 'Оплачено'),
        ('failed', 'Ошибка оплаты'),
        ('refunded', 'Возврат средств'),
    ]

    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending',
    )

    def __str__(self):
        return f"Order #{self.pk} - {self.get_payment_status_display()}"
    
    class Meta:
        verbose_name_plural = "Orders"

# Payment methods: crypto
class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment #{self.id}'
    
    class Meta:
        verbose_name_plural = "Payments"