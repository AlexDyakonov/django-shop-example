from django.db import models
from shortuuid.django_fields import ShortUUIDField
from userauths.models import User
from django.utils.html import mark_safe

STATUS_CHOICE = {
    ("process", "Processing"),
}

STATUS = {
    ("draft", "Draft"),
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
    
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=30, alphabet="abcdefgh12345")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=False)

    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directiory_path, null=False, default="product.png")
    description = models.CharField(null=False, blank=False, default="Товар в нашем магазине")

    price = models.DecimalField(max_digits=999999, decimal_places=2, default=9.99)
    old_price = models.DecimalField(max_digits=999999, decimal_places=2, default=14.99)

    in_stock = models.BooleanField(default=True)
    
    sku = ShortUUIDField(unique=True, length=4, max_length=10, prefix= "sku", alphabet="1234567890")

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self) -> str:
        return self.title
    
    def get_precentage(self):
        new_price = (self.price / self.old_price) * 100
        return new_price
    
    
