from django.db import models

class Planet(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)  # Assuming planet names are unique
    mass = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    radius = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = "Planet"
        verbose_name_plural = "Planets"

    def __str__(self):
        return self.name
