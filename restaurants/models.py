from django.contrib.gis.db import models
from users.models import User

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    location = models.PointField()
    waiters = models.ManyToManyField(User, related_name='restaurants')

    def __str__(self):
        return self.name