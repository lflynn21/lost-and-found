from django.urls import path

from . import views

app_name = 'googlemap'
urlpatterns = [
    path("", views.uva_building_map, name="uva_building_map"),
    path("save/<int:user_id>", views.save_location, name="save_location")
]