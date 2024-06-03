from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from .model_geographic_category import GeographicCategory
from .model_geographic_division import GeographicDivision
from .model_geographic_manager import GeographicManager

class GeographicPlace(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    elevation = models.FloatField(null=True, blank=True)
    confirmed = models.BooleanField(default=False)
    category = models.ForeignKey(GeographicCategory, on_delete=models.SET_DEFAULT, default=1)
    admin_division = models.ForeignKey(GeographicDivision, on_delete=models.CASCADE, related_name='places')
    location = gis_models.PointField(geography=True, null=True, blank=True)
    nearest_gfs_latitude = models.FloatField(null=True, blank=True)
    nearest_gfs_longitude = models.FloatField(null=True, blank=True)
    nearest_gfs_location = gis_models.PointField(geography=True, null=True, blank=True)

    objects = GeographicManager()

    class Meta:
        verbose_name = "Geographic Place"
        verbose_name_plural = "Geographic Places"

    def __str__(self):
        return f"{self.name or self.category.name} ({self.latitude}, {self.longitude})"

    def clean(self):
        if not self.admin_division:
            raise ValidationError('Place must be associated with a GeographicDivision.')
        if self.admin_division.level.name != 'Municipality':
            raise ValidationError(
                'Place can only be associated with a GeographicDivision at the Municipality level.'
            )

    def save(self, *args, **kwargs):
        self.clean()
        self.location = Point(self.longitude, self.latitude, srid=4326)
        if not self.elevation:
            self.elevation = 0
        if not self.name:
            self.name = "To Be Defined"
            similar_names = GeographicPlace.objects.filter(name__startswith=self.name).count()
            if similar_names > 0:
                self.name = f"{self.name} {similar_names + 1}"
        if not self.slug:
            self.slug = slugify(self.name)
            similar_slugs = GeographicPlace.objects.filter(slug__startswith=self.slug).count()
            if similar_slugs > 0:
                self.slug = f"{self.slug}-{similar_slugs + 1}"
        super().save(*args, **kwargs)

    def get_full_url(self):
        parts = [self.slug]
        admin_division = self.admin_division
        while admin_division:
            parts.append(admin_division.slug)
            admin_division = admin_division.parent
        if self.admin_division.country:
            parts.append(self.admin_division.country.slug)
            if self.admin_division.country.continent:
                parts.append(self.admin_division.country.continent.slug)
        return f"https://kairos.gr/geography/{'/'.join(reversed(parts))}"

    def get_weather_url(self):
        parts = [self.slug]
        admin_division = self.admin_division
        while admin_division:
            parts.append(admin_division.slug)
            admin_division = admin_division.parent
        if self.admin_division.country:
            parts.append(self.admin_division.country.slug)
            if self.admin_division.country.continent:
                parts.append(self.admin_division.country.continent.slug)
        return f"https://kairos.gr/weather/{'/'.join(reversed(parts))}"

    def update_nearest_gfs_coordinates(self, gfs_forecasts):
        min_distance = float('inf')
        nearest_forecast = None
        place_point = Point(self.longitude, self.latitude, srid=4326)
        for forecast in gfs_forecasts:
            forecast_point = Point(forecast.longitude, forecast.latitude, srid=4326)
            distance = place_point.distance(forecast_point)
            if distance < min_distance:
                min_distance = distance
                nearest_forecast = forecast
        if nearest_forecast:
            self.nearest_gfs_latitude = nearest_forecast.latitude
            self.nearest_gfs_longitude = nearest_forecast.longitude
            self.nearest_gfs_location = forecast_point
            self.save()