from django.db import models
from product.models import Product

# Create your models here.
class Part(Product):

    CATEGORY_CHOICES = [
        ('Carrocería', 'Carrocería'),
        ('Motor', 'Motor'),
        ('Transmisión', 'Transmisión'),
        ('Suspensión', 'Suspensión'),
        ('Ruedas', 'Ruedas'),
        ('Frenos', 'Frenos'),
        ('Manillar', 'Manillar'),
        ('Sistema de combustible', 'Sistema de combustible'),
        ('Chasis', 'Chasis')
    ]

    name = models.CharField(max_length=50)
    photo = models.URLField(blank=True, default="", max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    stock_quantity = models.PositiveIntegerField()
    manufacturer = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    