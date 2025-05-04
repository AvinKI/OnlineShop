from django.db import models
from django.utils import timezone
from Product.models import *


class Address(models.Model):
    user = models.ForeignKey('Account.CustomUser', on_delete=models.CASCADE, related_name='addresses')
    is_default = models.BooleanField(default=False)
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.address_line}, {self.city}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]
    user = models.ForeignKey('Account.CustomUser', on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        return sum(item.total_price for item in self.item.all())

    def __str__(self):
        return f"{self.user}, {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    price_at_order_time = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.quantity * self.price_at_order_time

    def __str__(self):
        return f"{self.product}, {self.quantity}"


class Shipment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    carrier = models.CharField(max_length=100)
    tracking_number = models.CharField(max_length=100)
    shipped_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.order}, {self.carrier}, {self.tracking_number}"


class Download(models.Model):
    user = models.ForeignKey('Account.CustomUser', on_delete=models.CASCADE, related_name='downloads')
    digital_product = models.ForeignKey(DigitalProduct, on_delete=models.CASCADE)
    download_url = models.URLField()
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.user}, {self.digital_product}, {self.download_url}"
