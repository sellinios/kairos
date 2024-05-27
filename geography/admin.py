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
    """
    Admin view for the Country model.
    """
    list_display = [
        'name', 'iso_alpha2', 'iso_alpha3', 'iso_numeric', 'continent',
        'capital', 'fetch_forecasts'
    ]
    search_fields = ['name', 'iso_alpha2', 'iso_alpha3', 'iso_numeric']
    list_filter = ['fetch_forecasts']

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    """
    Admin view for the Level model.
    """
    list_display = ['name', 'level_order']
    list_filter = ['name']
    search_fields = ['name']

@admin.register(AdminDivisionInstance)
class AdminDivisionInstanceAdmin(admin.ModelAdmin):
    """
    Admin view for the AdminDivisionInstance model.
    """
    list_display = ['name', 'level', 'parent']
    list_filter = ['level']
    search_fields = ['name']

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    """
    Admin view for the Place model.
    """
    list_display = [
        'id', 'longitude', 'latitude', 'height', 'category',
        'admin_division'
    ]
    search_fields = [
        'id', 'longitude', 'latitude', 'category__name',
        'admin_division__name'
    ]
    list_filter = ['category', 'admin_division']

    def get_form(self, request, obj=None, change=False, **kwargs):
        """
        Override the default form to make the admin_division field optional.
        """
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields['admin_division'].required = False
        return form
