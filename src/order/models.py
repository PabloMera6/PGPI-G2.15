from django.db import models
from product.models import Product

# Create your models here.
class Order(models.Model):
    SHIPMENT_CHOICES = [
        ('Recogida', 'Recogida'),
        ('Envío a domicilio', 'Envío a domicilio'),
    ]

    STATE_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Confirmado', 'Confirmado'),
        ('Entregado', 'Entregado'),
        ('En reparto', 'En reparto'),
    ]

    PAYMENT_CHOICES = [
        ('Contrarrembolso', 'Contrarrembolso'),
        ('Tarjeta', 'Tarjeta'),
    ]


    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey('users.UserProfile', on_delete=models.CASCADE,null=True)
    state = models.CharField(max_length=50, choices=STATE_CHOICES, default='pending')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    shipment = models.CharField(max_length=50, choices=SHIPMENT_CHOICES, default='pickup')
    address = models.CharField(max_length=255, null=True)
    products = models.ManyToManyField(Product, through='OrderProduct')
    payment = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default='cash')
    buyer_mail = models.EmailField(max_length=254,null=False,blank=False,default='a@a.com')
    buyer_name = models.CharField(max_length=50,null=False,blank=False,default='a')
    buyer_phone = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=50,null=False,blank=False,default='a')
    postal_code = models.CharField(max_length=5,null=False,blank=False,default='41720')

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
