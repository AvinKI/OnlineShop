from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name





class Product(models.Model):
    class Availability(models.TextChoices):
        IN_STOCK = "in_stock", _("In stock")
        OUT_OF_STOCK = "out_of_stock", _("Out of stock")
        COMING_SOON = "coming_soon", _("Coming soon")

    name = models.CharField(max_length=255)
    is_digit = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)])
    discount_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    availability = models.CharField(max_length=20, choices=Availability.choices, default=Availability.IN_STOCK)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='products/images/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def has_discount(self):
        return self.discount_price is not None and self.discount_price < self.price

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']



class DigitalProduct(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='digital_data',
        null=True,
        blank=True
    )
    file = models.FileField(upload_to='digital_products/')



class PhysicalProduct(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name='physical_data',
        null=True,
    )
    stock = models.PositiveIntegerField(default=0)
    weight = models.DecimalField(max_digits=6, decimal_places=2, help_text='kg')
    length = models.DecimalField(max_digits=6, decimal_places=2, help_text='cm')
    width = models.DecimalField(max_digits=6, decimal_places=2, help_text='cm')
    height = models.DecimalField(max_digits=6, decimal_places=2, help_text='cm')
