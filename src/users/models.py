from django.db import models

# Create your models here.
class UserProfile(models.Model):
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    phone = models.CharField(max_length=20,blank=True, null=True)
    full_name = models.CharField(max_length=255,blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    