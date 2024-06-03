"""
Admin configuration for the geography app.
"""

from django.contrib import admin
from django.contrib import messages
import googlemaps
from django.conf import settings
from .models import (
    GeographicPlanet,
    GeographicContinent,
    GeographicCategory,
    GeographicCountry,
    GeographicLevel,
    GeographicDivision,
    GeographicPlace
)

admin.site.register(GeographicPlanet)
admin.site.register(GeographicContinent)
admin.site.register(GeographicCategory)

@admin.register(GeographicCountry)
class CountryAdmin(admin.ModelAdmin):
    """Admin configuration for GeographicCountry model."""
    list_display = [
        'name', 'iso_alpha2', 'iso_alpha3', 'iso_numeric', 'continent',
        'capital', 'fetch_forecasts'
    ]
    search_fields = ['name', 'iso_alpha2', 'iso_alpha3', 'iso_numeric']
    list_filter = ['fetch_forecasts']

@admin.register(GeographicLevel)
class LevelAdmin(admin.ModelAdmin):
    """Admin configuration for GeographicLevel model."""
    list_display = ['name', 'level_order']
    list_filter = ['name']
    search_fields = ['name']

@admin.register(GeographicDivision)
class DivisionAdmin(admin.ModelAdmin):
    """Admin configuration for GeographicDivision model."""
    list_display = ['name', 'level', 'parent', 'slug']
    list_filter = ['level']
    search_fields = ['name']

@admin.register(GeographicPlace)
class PlaceAdmin(admin.ModelAdmin):
    """Admin configuration for GeographicPlace model."""
    list_display = [
        'id', 'name', 'longitude', 'latitude', 'elevation', 'category',
        'admin_division', 'confirmed', 'slug'
    ]
    search_fields = [
        'id', 'name', 'longitude', 'latitude', 'category__name',
        'admin_division__name'
    ]
    list_filter = ['category', 'admin_division', 'confirmed']

    def get_form(self, request, obj=None, change=False, **kwargs):
        """Override the default form to make admin_division field required."""
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields['admin_division'].required = True
        return form

    actions = ['update_elevation_and_admin_levels']

    def update_elevation_and_admin_levels(self, request, queryset):
        """Action to update elevation and administrative levels for selected places."""
        api_key = settings.GOOGLE_MAPS_API_KEY
        if not api_key:
            self.message_user(
                request, 'Google Maps API key is not set in settings', messages.ERROR
            )
            return

        gmaps = googlemaps.Client(key=api_key)
        updated_count = 0

        for place in queryset:
            try:
                self.update_place_elevation(gmaps, place)
                self.update_place_admin_divisions(gmaps, place)
                place.save()
                updated_count += 1

            except Exception as e:  # pylint: disable=broad-exception-caught
                self.message_user(
                    request, f'Error updating place {place.name}: {e}', messages.ERROR
                )

        self.message_user(
            request, f'Successfully updated elevation and administrative levels for {updated_count} places.', messages.SUCCESS
        )

    update_elevation_and_admin_levels.short_description = 'Update elevation and administrative levels for selected places'

    def update_place_elevation(self, gmaps, place):
        """Update the elevation of a place."""
        elevation_result = gmaps.elevation((place.latitude, place.longitude))
        elevation = elevation_result[0]['elevation'] if elevation_result else None
        if elevation is not None:
            place.elevation = elevation

    def update_place_admin_divisions(self, gmaps, place):
        """Update the administrative divisions of a place."""
        geocode_result = gmaps.reverse_geocode((place.latitude, place.longitude))
        if geocode_result:
            admin_divisions = self._extract_admin_divisions(geocode_result)

            country, _ = GeographicCountry.objects.get_or_create(
                name=admin_divisions.get('country', '')
            )
            admin_area_1 = self._get_or_create_admin_division(
                admin_divisions.get('admin_area_1', ''), 'Region', country
            )
            admin_area_2 = self._get_or_create_admin_division(
                admin_divisions.get('admin_area_2', ''), 'Municipality', country, admin_area_1
            )

            place.admin_division = admin_area_2

    def _extract_admin_divisions(self, geocode_result):
        """Extract administrative divisions from geocode result."""
        address_components = geocode_result[0]['address_components']
        admin_divisions = {}

        for component in address_components:
            if 'country' in component['types']:
                admin_divisions['country'] = component['long_name']
            elif 'administrative_area_level_1' in component['types']:
                admin_divisions['admin_area_1'] = component['long_name']
            elif 'administrative_area_level_2' in component['types']:
                admin_divisions['admin_area_2'] = component['long_name']
            elif 'locality' in component['types']:
                admin_divisions['locality'] = component['long_name']

        return admin_divisions

    def _get_or_create_admin_division(self, name, level_name, country, parent=None):
        """Get or create an administrative division."""
        level = GeographicLevel.objects.get(name=level_name)  # pylint: disable=no-member
        division, _ = GeographicDivision.objects.get_or_create(
            name=name,
            level=level,
            parent=parent,
            country=country
        )
        return division
