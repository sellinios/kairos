from django.contrib import admin
from .models import GFSParameter, GFSConfig

class GFSParameterAdmin(admin.ModelAdmin):
    """
    Admin view for GFSParameter model.
    """
    list_display = (
        'name', 'description', 'level', 'type_of_level', 'parameter_id', 'last_updated'
    )  # Fields to display in the list view
    search_fields = ('name', 'description', 'parameter_id')  # Fields to include in the search bar
    list_filter = ('level', 'type_of_level')  # Fields to filter by in the admin interface

class GFSConfigAdmin(admin.ModelAdmin):
    """
    Admin view for GFSConfig model.
    """
    filter_horizontal = ('countries', 'parameters')
    list_display = ('id', 'get_countries', 'get_parameters', 'forecast_hours')

    def get_countries(self, obj):
        return ", ".join([country.name for country in obj.countries.all()])
    get_countries.short_description = 'Countries'

    def get_parameters(self, obj):
        return ", ".join([f"{parameter.name} (ID: {parameter.parameter_id})" for parameter in obj.parameters.all()])
    get_parameters.short_description = 'Parameters'

admin.site.register(GFSParameter, GFSParameterAdmin)
admin.site.register(GFSConfig, GFSConfigAdmin)
