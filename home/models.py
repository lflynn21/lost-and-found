import datetime

from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.validators import MinValueValidator

CATEGORIES = [
    ("Water Bottle", "Water Bottle"),
    ("Keys", "Keys"),
    ("Friend", "Friend"),
    ("ID Card", "ID Card"),
    ("Wallet","Wallet"),
    ("Cell Phones","Cell Phones"),
    ("Laptops/Tablets","Laptops/Tablets"),
    ("Headphones","Headphones"),
    ("Umbrellas","Umbrellas"),
    ("Clothing/Accessories","Clothing/Accessories"),
    ("Others","Others - Specify in description")
]

NEW_HUB = [
    ("Yes", "Yes"),
    ("No", "No"),
]

class Location(models.Model):
    latitude = models.DecimalField(max_digits=25, decimal_places=17)
    longitude = models.DecimalField(max_digits=25, decimal_places=17)

    def __str__(self):
        return f"{self.latitude}, {self.longitude}"
    
class Hub(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="Hub Name")
    description = models.TextField(verbose_name="Hub Location Description")

    approved = models.BooleanField(default=False)
    def __str__(self):
        return self.name + " - " + self.description


# Create your models here.
class LostItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    category = models.CharField(max_length=200, choices=CATEGORIES)
    description = models.CharField(max_length=200)
    # Reward validated >= 0 source:
    # https://stackoverflow.com/questions/54858123/how-do-i-enforce-a-positive-number-on-my-python-django-model-field
    reward = models.FloatField(default=0.00, null=False, validators=[MinValueValidator(0)])
    sub_date = models.DateTimeField("date submitted", default=timezone.now)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.category + " lost by " + self.user.username


# Create your models here.
class FoundItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    category = models.CharField(max_length=200, choices=CATEGORIES)
    item_description = models.CharField(max_length=200)
    found_date = models.DateTimeField("date reported found", default=timezone.now)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    hub = models.ForeignKey(Hub, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.category+" found by "+self.user.username
