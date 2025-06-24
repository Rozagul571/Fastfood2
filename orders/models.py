
from django.db import models
from django.contrib.gis.db import models as gis_models
from users.models import User
from restaurants.models import Restaurant
from dishes.models import Dish

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACCEPTED = 'accepted', 'Accepted'
        PREPARING = 'preparing', 'Preparing'
        DELIVERING = 'delivering', 'Delivering'
        DELIVERED = 'delivered', 'Delivered'
        CANCELLED = 'cancelled', 'Cancelled'

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='orders')  # SAQLANDI: Buyurtma foydalanuvchisi
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders')  # SAQLANDI: Restoran
    status = models.CharField(max_length=20, choices=Status.choices,
                              default=Status.PENDING)  # SAQLANDI: Buyurtma holati
    delivery_address = models.CharField(max_length=255)  # SAQLANDI: Yetkazib berish manzili
    location = gis_models.PointField()  # SAQLANDI: Foydalanuvchi lokatsiyasi
    distance_km = models.FloatField(null=True, blank=True)  # SAQLANDI: Masofa (km)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True,
                                       blank=True)  # SAQLANDI: Yetkazib berish narxi
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # SAQLANDI: Umumiy narx
    estimated_time = models.IntegerField(null=True, blank=True)  # SAQLANDI: Taxminiy yetkazib berish vaqti
    created_at = models.DateTimeField(auto_now_add=True)  # SAQLANDI: Yaratilgan vaqt
    updated_at = models.DateTimeField(auto_now=True)  # SAQLANDI: Yangilangan vaqt


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')  # SAQLANDI: Buyurtma
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)  # SAQLANDI: Taom
    quantity = models.PositiveIntegerField()  # SAQLANDI: Miqdor
    price = models.DecimalField(max_digits=10, decimal_places=2)  # SAQLANDI: Bir dona taom narxi

    def __str__(self):
        return f"{self.quantity} x {self.dish.name}"


