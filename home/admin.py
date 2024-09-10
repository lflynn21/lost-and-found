from django.contrib import admin

from .models import LostItem, FoundItem, Location, Hub
# Register your models here.

admin.site.register(LostItem)
admin.site.register(FoundItem)
admin.site.register(Location)
admin.site.register(Hub)