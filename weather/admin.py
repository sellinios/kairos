from django.contrib import admin
from .models import GFSForecast
from .forms import GFSForecastForm

class GFSForecastAdmin(admin.ModelAdmin):
    form = GFSForecastForm

admin.site.register(GFSForecast, GFSForecastAdmin)
