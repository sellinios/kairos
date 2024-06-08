from django.contrib import admin
from .models import GFSParameter

@admin.register(GFSParameter)
class GFSParameterAdmin(admin.ModelAdmin):
    list_display = ('number', 'level_layer', 'parameter', 'forecast_valid', 'description', 'last_updated')
    search_fields = ('number', 'parameter', 'level_layer')
