from django.contrib import admin
from .models import Country, Region, RegionalUnit, Municipality, Place
from .forms import PlaceForm

admin.site.register(Country)
admin.site.register(Region)
admin.site.register(RegionalUnit)
admin.site.register(Municipality)

class PlaceAdmin(admin.ModelAdmin):
    form = PlaceForm

admin.site.register(Place, PlaceAdmin)
