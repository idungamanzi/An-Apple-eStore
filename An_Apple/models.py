from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.timezone import now

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    product_type = models.CharField(
    max_length=50,
    choices=[
        ('phone', 'Phone'),
        ('charger', 'Charger'),
        ('cable', 'Cable'),
        ('cover', 'Cover'),
    ],
    default='phone'  # Provide a sensible default
)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='product_images/')
    stock_quantity = models.IntegerField(default=0)
    category = models.CharField(max_length=100, default="All Categories")
    is_featured = models.BooleanField(default=False)
    condition = models.CharField(max_length=50, choices=[('new', 'Brand New'), ('used', 'Used'), ('pre_owned', 'Pre-Owned')], default='new')
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    @property
    def discount_percentage(self):
        if self.original_price and self.original_price > self.price:
            return round((self.original_price - self.price) / self.original_price * 100)
        return None


    def __str__(self):
        return self.name

class Cart(models.Model):
    session_key = models.CharField(max_length=255, unique=True, default='')
    created_at = models.DateTimeField(default=timezone.now) 
    updated_at = models.DateTimeField(default=timezone.now) 

    def __str__(self):
        return f"Cart {self.id} - Session {self.session_key}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items',  default=1)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    proof_of_payment = models.FileField(upload_to='proofs/')
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)