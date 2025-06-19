from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as gis_models
from django.db import models
from .managers import CustomUserManager

class User(AbstractUser):
    class RoleType(models.TextChoices):
        ADMIN = "admin", "Admin"
        WAITER = "waiter", "Waiter"
        USER = "user", "User"
    role = models.CharField(max_length=10, choices=RoleType.choices, default=RoleType.USER)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    location = gis_models.PointField(geography=True, null=True, blank=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'phone_number'
    username = None
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.phone_number} ({self.role})"