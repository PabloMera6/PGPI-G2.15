from django.db import models

# Create your models here.
class Manufacturer():

    name = models.CharField(max_length=50)
    photo = models.URLField(blank=True, default="", max_length=200)

    def __str__(self):
        return self.name