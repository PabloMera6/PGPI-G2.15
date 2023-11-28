from django.db import models
from users.models import UserProfile



# Create your models here.
class Claim(models.Model):

    

    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    title = models.TextField(max_length=100, default="Sin título")
    description = models.TextField(max_length=500)
    response = models.TextField(max_length=500, blank=True, null=True)

