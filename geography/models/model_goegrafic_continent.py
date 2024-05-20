from django.db import models

class Continent(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Continent"
        verbose_name_plural = "Continents"

    def __str__(self):
        return self.name