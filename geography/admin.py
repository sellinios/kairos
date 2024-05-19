from django.contrib import admin
from .models.planet import Planet
from .models.continent import Continent
from .models.country import Country
from .models.administrative_division import AdministrativeDivision
from .models.geographic_entity import GeographicEntity
from .models.place import Place

admin.site.register(Planet)
admin.site.register(Continent)
admin.site.register(Country)
admin.site.register(AdministrativeDivision)
admin.site.register(GeographicEntity)
admin.site.register(Place)
