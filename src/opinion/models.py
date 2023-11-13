from django.db import models
from users.models import UserProfile
from product.models import Product


# Create your models here.
class Opinion(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    description = models.TextField(max_length=500)