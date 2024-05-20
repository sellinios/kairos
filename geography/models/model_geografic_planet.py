from django.db import models

class Planet(models.Model):
    name = models.CharField(max_length=100)
    mass = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
    radius = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = "Planet"
        verbose_name_plural = "Planets"

    def __str__(self):
        return self.name
