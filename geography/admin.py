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
    list_display = ['name', 'iso_alpha2', 'iso_alpha3', 'iso_numeric', 'continent', 'capital']
    search_fields = ['name', 'iso_alpha2', 'iso_alpha3', 'iso_numeric']

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'level_order']
    list_filter = ['name']
    search_fields = ['name']

@admin.register(AdminDivisionInstance)
class AdminDivisionInstanceAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'parent']
    list_filter = ['level']
    search_fields = ['name']

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['id', 'longitude', 'latitude', 'height', 'category', 'admin_division']
    search_fields = ['id', 'longitude', 'latitude', 'category__name', 'admin_division__name']
    list_filter = ['category', 'admin_division']

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['admin_division'].required = False  # Make optional
        return form
