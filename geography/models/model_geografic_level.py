from django.db import models
from .model_geografic_country import Country

class Level(models.Model):
    name = models.CharField(max_length=100)
    level_order = models.IntegerField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='levels')

    class Meta:
        unique_together = ('name', 'country')

    def __str__(self):
        return self.name
