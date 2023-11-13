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
        ('Electricidad', 'Electricidad'),
        ('Manillar', 'Manillar'),
        ('Sistema de combustible', 'Sistema de combustible'),
        ('chasis', 'chasis')
    ]

    name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='part_photos/', null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    stock_quantity = models.PositiveIntegerField()
    manufacturer = models.CharField(max_length=255)
    