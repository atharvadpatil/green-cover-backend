from django.urls import path
from .views import home

urlpatterns = [
    path('foliumexample', home.as_view(), name="home"),
]