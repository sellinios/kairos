from django.contrib import admin
from .models import Country, Region, RegionalUnit, Municipality, Place
from .forms import PlaceForm  # Ensure this import is correct and PlaceForm is defined in forms.py

# Import the GFSForecast model from the weather app
from weather.models import GFSForecast

# Register other models normally
admin.site.register(Country)
admin.site.register(Region)
admin.site.register(RegionalUnit)
admin.site.register(Municipality)

# Define the custom admin class for Place
class PlaceAdmin(admin.ModelAdmin):
    form = PlaceForm

# Use the custom admin class when registering Place
admin.site.register(Place, PlaceAdmin)

# Define the custom admin class for GFSForecast
class GFSForecastAdmin(admin.ModelAdmin):
    list_display = ('place', 'timestamp')
    search_fields = ('place__name', 'timestamp')
    list_filter = ('place', 'timestamp')

# Register the GFSForecast model
admin.site.register(GFSForecast, GFSForecastAdmin)
