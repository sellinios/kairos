# weather/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Define your URL patterns here
    path('forecasts/', views.GFSForecastListView.as_view(), name='forecast-list'),
    # Add more paths as needed
]