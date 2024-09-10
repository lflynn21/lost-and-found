from django.urls import path

from . import views

app_name = 'home'
urlpatterns = [
    path("", views.index, name="index"),
    path("lost-items", views.lost_items, name="lost-items"),
    path("found-items", views.found_items, name="found-items"),
    path("hubs", views.hubs, name="hubs"),
    path("report-lost-item", views.lost_item_form, name="report-lost"),
    path("report-found-item", views.found_item_form, name="report-found"),
    path("lost-detail/<int:pk>/", views.lost_detail, name="lost-detail"),
    path("found-detail/<int:pk>/", views.found_detail, name="found-detail"),
    path("claimed-item/<int:pk>/", views.claimed_item, name="claimed-item"),
    path("request-hub", views.hub_form, name="request-hub"),
    path("approve-hubs", views.approve_hubs, name="approve-hubs"),
    path("approve-hub/<int:hub>", views.approve_hub, name="approve-hub"),
    path('hub-detail/<int:pk>/', views.HubDetailView.as_view(), name='hub-detail'),
]