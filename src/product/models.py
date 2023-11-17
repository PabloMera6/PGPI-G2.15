from django.db import models
from manufacturer.models import Manufacturer

# Create your models here.

class Product(models.Model):
    TYPE_CHOICES = [
        ('M', 'Motorcycle'),
        ('P', 'Part'),
    ]
    reference_number =  models.CharField(max_length=15,unique=True)
    product_type = models.CharField(max_length=1,choices=TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, default=None, related_name='manufacturer')