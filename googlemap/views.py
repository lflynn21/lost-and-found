from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Location


def uva_building_map(request):
    building_coordinates = {
        'latitude': 38.0359,
        'longitude': -78.5037,
    }
    return render(request, 'googlemap/index.html', {'building_coordinates': building_coordinates})

def save_location(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    latitude = request.POST['latitude']
    longitude = request.POST['longitude']
    location = Location(user=user, latitude=latitude, longitude=longitude)
    location.save()
    return HttpResponseRedirect(reverse("home:index", ))