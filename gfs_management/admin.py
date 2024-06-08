from django.contrib import admin
from django.db import models
from .models import GFSParameter

# Define the custom admin action
def disable_selected_parameters(modeladmin, request, queryset):
    queryset.update(enabled=False)
    modeladmin.message_user(request, "Selected parameters have been disabled.")

disable_selected_parameters.short_description = "Disable selected parameters"

@admin.register(GFSParameter)
class GFSParameterAdmin(admin.ModelAdmin):
    list_display = ('number', 'level_layer', 'parameter', 'forecast_valid', 'description', 'enabled', 'last_updated')
    list_editable = ('enabled',)
    search_fields = ('number', 'parameter', 'level_layer')
    list_filter = ('enabled',)
    actions = [disable_selected_parameters]  # Add the custom action
