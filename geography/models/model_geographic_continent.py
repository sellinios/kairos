# geography/models/model_geographic_continent.py
from django.db import models
from django.utils.text import slugify

class Continent(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = "Continent"
        verbose_name_plural = "Continents"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Continent, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
