from django.urls import path
from .views import (
    home, 
    airQualityIndexView, 
    landCoverView, 
    ndviTimelapseView, 
    vegetationView, 
    VolunteerView, 
    AdminView, 
    EventView,
    GetEventView,
    StatiscticsView
)

urlpatterns = [
    path('foliumexample', home.as_view(), name="home"),
    path('airqualityindex', airQualityIndexView.as_view(), name="airqualityindex"),
    path('landcover', landCoverView.as_view(), name="landcover"),
    path('ndvitimelapse', ndviTimelapseView.as_view(), name="ndvitimelapse"),
    path('vegetation', vegetationView.as_view(), name="vegetation"),

    path('create-volunteer', VolunteerView.as_view(), name="create-volunteer"),
    path('get-volunteers', AdminView.as_view(), name="get-volunteers"),

    path('create-event', EventView.as_view(), name="create-event"),
    path('get-event', GetEventView.as_view(), name="get-event"),

    path('statistics', StatiscticsView.as_view(), name="statistics"),

]