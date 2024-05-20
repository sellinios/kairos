from django.db import models

class GeographicEntity(models.Model):
    ENTITY_TYPES = (
        ('country', 'Country'),
        ('region', 'Region'),
        ('locality', 'Locality'),
        # Add other entity types as needed
    )

    name = models.CharField(max_length=100)
    entity_type = models.CharField(max_length=20, choices=ENTITY_TYPES)

    def __str__(self):
        return self.name
