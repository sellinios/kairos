"""
Admin configuration for GFS management application.
"""

from django.contrib import admin
from .models import GFSParameter, GFSConfig


class GFSParameterAdmin(admin.ModelAdmin):
    """
    Admin view for GFSParameter model.
    """
    list_display = (
        'name', 'description', 'level', 'type_of_level'
    )  # Fields to display in the list view
    search_fields = ('name', 'description')  # Fields to include in the search bar
    list_filter = ('level', 'type_of_level')  # Fields to filter by in the admin interface


class GFSConfigAdmin(admin.ModelAdmin):
    """
    Admin view for GFSConfig model.
    """
    filter_horizontal = ('countries', 'parameters')


admin.site.register(GFSParameter, GFSParameterAdmin)
admin.site.register(GFSConfig, GFSConfigAdmin)
