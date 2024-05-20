from django.contrib import admin
from .models.model_geografic_planet import Planet
from .models.model_goegrafic_continent import Continent
from .models.model_geografic_country import Country
from .models.model_geografic_administrative_division import AdministrativeDivision
from .models.model_geographic_entity import GeographicEntity
from .models.model_geografic_place import Place

admin.site.register(Planet)
admin.site.register(Continent)
admin.site.register(Country)
admin.site.register(AdministrativeDivision)
admin.site.register(GeographicEntity)
admin.site.register(Place)
