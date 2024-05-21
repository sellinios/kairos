from django.db import models

class Continent(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)  # Assuming continent names are unique

    class Meta:
        verbose_name = "Continent"
        verbose_name_plural = "Continents"

    def __str__(self):
        return self.name
