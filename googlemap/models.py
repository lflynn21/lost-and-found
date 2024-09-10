from django.db import models
from django.conf import settings

# Create your models here.

class Location(models.Model):
    latitude = models.DecimalField(max_digits=25, decimal_places=17)
    longitude = models.DecimalField(max_digits=25, decimal_places=17)

    def __str__(self):
        return f"{self.latitude}, {self.longitude}"