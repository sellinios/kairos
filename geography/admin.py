# geography/admin.py
from django.contrib import admin
from django.contrib import messages
from .models import Planet, Continent, Country, Level, AdminDivisionInstance, Place, Category
import googlemaps
from django.conf import settings

admin.site.register(Planet)
admin.site.register(Continent)
admin.site.register(Category)

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'iso_alpha2', 'iso_alpha3', 'iso_numeric', 'continent',
        'capital', 'fetch_forecasts'
    ]
    search_fields = ['name', 'iso_alpha2', 'iso_alpha3', 'iso_numeric']
    list_filter = ['fetch_forecasts']

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'level_order']
    list_filter = ['name']
    search_fields = ['name']

@admin.register(AdminDivisionInstance)
class AdminDivisionInstanceAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'parent', 'slug']
    list_filter = ['level']
    search_fields = ['name']

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'longitude', 'latitude', 'elevation', 'category',
        'admin_division', 'confirmed', 'slug'
    ]
    search_fields = [
        'id', 'name', 'longitude', 'latitude', 'category__name',
        'admin_division__name'
    ]
    list_filter = ['category', 'admin_division', 'confirmed']

    # Ensure the admin_division is required
    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields['admin_division'].required = True
        return form

    actions = ['update_elevation_and_admin_levels']

    def update_elevation_and_admin_levels(self, request, queryset):
        api_key = settings.GOOGLE_MAPS_API_KEY
        if not api_key:
            self.message_user(request, 'Google Maps API key is not set in settings', messages.ERROR)
            return

        gmaps = googlemaps.Client(key=api_key)
        updated_count = 0

        for place in queryset:
            try:
                # Fetch elevation data
                elevation_result = gmaps.elevation((place.latitude, place.longitude))
                elevation = elevation_result[0]['elevation'] if elevation_result else None

                if elevation is not None:
                    place.elevation = elevation

                # Fetch geolocation details
                geocode_result = gmaps.reverse_geocode((place.latitude, place.longitude))
                if geocode_result:
                    address_components = geocode_result[0]['address_components']

                    # Extract administrative levels
                    admin_divisions = {}
                    for component in address_components:
                        if 'country' in component['types']:
                            admin_divisions['country'] = component['long_name']
                        elif 'administrative_area_level_1' in component['types']:
                            admin_divisions['admin_area_1'] = component['long_name']
                        elif 'administrative_area_level_2' in component['types']:
                            admin_divisions['admin_area_2'] = component['long_name']
                        elif 'administrative_area_level_3' in component['types']:
                            admin_divisions['admin_area_3'] = component['long_name']
                        elif 'locality' in component['types']:
                            admin_divisions['locality'] = component['long_name']

                    # Update or create administrative divisions
                    country, _ = Country.objects.get_or_create(name=admin_divisions.get('country', ''))
                    admin_area_1, _ = AdminDivisionInstance.objects.get_or_create(
                        name=admin_divisions.get('admin_area_1', ''), level=Level.objects.get(name='Admin Area 1'), country=country)
                    admin_area_2, _ = AdminDivisionInstance.objects.get_or_create(
                        name=admin_divisions.get('admin_area_2', ''), level=Level.objects.get(name='Admin Area 2'), parent=admin_area_1, country=country)
                    admin_area_3, _ = AdminDivisionInstance.objects.get_or_create(
                        name=admin_divisions.get('admin_area_3', ''), level=Level.objects.get(name='Admin Area 3'), parent=admin_area_2, country=country)

                    place.admin_division = admin_area_3
                    place.save()
                    updated_count += 1

                else:
                    self.message_user(request, f'Could not fetch geolocation details for place: {place.name}', messages.ERROR)

            except Exception as e:
                self.message_user(request, f'Error updating place {place.name}: {e}', messages.ERROR)

        self.message_user(request, f'Successfully updated elevation and administrative levels for {updated_count} places.', messages.SUCCESS)

    update_elevation_and_admin_levels.short_description = 'Update elevation and administrative levels for selected places'
