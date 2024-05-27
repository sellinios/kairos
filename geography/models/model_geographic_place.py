from django.contrib.gis.db import models as gis_models
from django.db import models
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from .model_geographic_category import Category
from .model_geographic_admin_division import AdminDivisionInstance
from .model_geographic_place_manager import PlaceManager
from django.apps import apps

class Place(models.Model):
    """
    Represents a geographic place.
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    elevation = models.FloatField(null=True, blank=True)
    confirmed = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1)
    admin_division = models.ForeignKey(AdminDivisionInstance, on_delete=models.CASCADE, related_name='places')
    location = gis_models.PointField(geography=True, null=True, blank=True)

    objects = PlaceManager()

    class Meta:
        verbose_name = "Place"
        verbose_name_plural = "Places"

    def __str__(self):
        """
        Return a string representation of the Place instance.
        """
        return f"{self.name or self.category.name} ({self.latitude}, {self.longitude})"

    def clean(self):
        """
        Validate the Place instance before saving.
        """
        if self.admin_division.level.name != 'Municipality':
            raise ValidationError('Place can only be associated with an AdminDivisionInstance at the Municipality level.')

    def save(self, *args, **kwargs):
        self.clean()
        self.location = Point(self.longitude, self.latitude, srid=4326)

        if not self.height:
            self.height = 0  # Default height if elevation is not provided

        if not self.name:
            self.name = "To Be Defined"
            similar_names = Place.objects.filter(name__startswith=self.name).count()
            if similar_names > 0:
                self.name = f"{self.name} {similar_names + 1}"

        # Generate slug
        if not self.slug:
            self.slug = slugify(self.name)
            similar_slugs = Place.objects.filter(slug__startswith=self.slug).count()
            if similar_slugs > 0:
                self.slug = f"{self.slug}-{similar_slugs + 1}"

        super().save(*args, **kwargs)

    def get_full_url(self):
        """
        Generate the full URL for the Place based on its administrative divisions.
        """
        parts = [self.slug]
        admin_division = self.admin_division

        while admin_division:
            parts.append(admin_division.slug)
            admin_division = admin_division.parent

        return f"https://kairos.gr/geography/{'/'.join(reversed(parts))}"
