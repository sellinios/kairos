"""
Admin configuration for the weather app.
"""

from django.contrib import admin
from .models import GFSForecast, MetarStation, MetarData
from .forms import GFSForecastForm

class GFSForecastAdmin(admin.ModelAdmin):
    """
    Admin view for the GFSForecast model.
    """
    form = GFSForecastForm

admin.site.register(GFSForecast, GFSForecastAdmin)

class MetarDataInline(admin.TabularInline):
    """
    Inline admin view for the MetarData model.
    """
    model = MetarData
    extra = 0
    readonly_fields = ('metar_text', 'timestamp', 'metar_timestamp')

class MetarStationAdmin(admin.ModelAdmin):
    """
    Admin view for the MetarStation model.
    """
    list_display = ('name', 'code', 'longitude', 'latitude')
    inlines = [MetarDataInline]
    actions = ['fetch_and_update_location']

    def longitude(self, obj):
        """
        Return the longitude of the MetarStation.
        """
        return obj.location.x if obj.location else None

    def latitude(self, obj):
        """
        Return the latitude of the MetarStation.
        """
        return obj.location.y if obj.location else None

    longitude.short_description = 'Longitude'
    latitude.short_description = 'Latitude'

    def fetch_and_update_location(self, request, queryset):
        """
        Fetch and update the GIS location for selected MetarStations.
        """
        for station in queryset:
            if station.update_location():
                self.message_user(request, f"Updated location for {station.name}")
            else:
                self.message_user(request, f"Failed to update location for {station.name}", level='error')
    fetch_and_update_location.short_description = "Fetch and update GIS location"

admin.site.register(MetarStation, MetarStationAdmin)
