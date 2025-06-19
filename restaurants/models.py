from django.db import models
from django.contrib.gis.db import models as gis_models

class Restaurant(models.Model):
    class CuisineType(models.TextChoices):
        FASTFOOD = "fastfood", "Fast Food"
        NATIONALFOOD = "national", "National Food"
        OTHER = "other", "Other"
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    location = gis_models.PointField(geography=True)
    waiters = models.ManyToManyField('users.User', related_name='restaurants')

    def __str__(self):
        return self.name