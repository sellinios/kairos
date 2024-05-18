from django.contrib import admin
from .models import GFSForecast
from .forms import GFSForecastForm
from .models import MetarStation, MetarData


class GFSForecastAdmin(admin.ModelAdmin):
    form = GFSForecastForm


admin.site.register(GFSForecast, GFSForecastAdmin)


class MetarDataInline(admin.TabularInline):
    model = MetarData
    extra = 0
    readonly_fields = ('metar_text', 'timestamp', 'metar_timestamp')


class MetarStationAdmin(admin.ModelAdmin):
    list_display = ('name', 'longitude', 'latitude')
    inlines = [MetarDataInline]


admin.site.register(MetarStation, MetarStationAdmin)
