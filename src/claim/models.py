from django.db import models
from users.models import UserProfile



# Create your models here.
class Claim(models.Model):

    

    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=500)
