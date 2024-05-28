"""
Admin configuration for the geography app.
"""

from django.contrib import admin
from .models.model_geographic_planet import Planet
from .models.model_geographic_continent import Continent
from .models.model_geographic_country import Country
from .models.model_geographic_level import Level
from .models.model_geographic_admin_division import AdminDivisionInstance
from .models.model_geographic_place import Place
from .models.model_geographic_category import Category

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