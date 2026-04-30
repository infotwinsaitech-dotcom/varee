from django.db import models
from django.contrib.auth.models import User
from backend.products.models import Product


class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.TextField()
    payment_method = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    cancel_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - Order {self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)