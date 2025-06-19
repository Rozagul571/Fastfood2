from decimal import Decimal
from django.db import models
from django.contrib.gis.db.models import PointField
from orders.utils import calculate_distance, calculate_totals, estimate_delivery

class Order(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'pending','Pending'
        ACCEPTED = 'accepted','Accepted'
        PREPARING = 'preparing','Preparing'
        DELIVERING = 'delivering','Delivering'
        DELIVERED = 'delivered','Delivered'
        CANCELLED = 'cancelled','Cancelled'

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='orders')
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    delivery_address = models.TextField()
    location = PointField(geography=True)
    distance_km = models.DecimalField(max_digits=7, decimal_places=3, default=0)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_quantity = models.PositiveIntegerField(default=0)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estimated_time = models.PositiveIntegerField(default=0)
    preparation_time = models.PositiveIntegerField(default=0)
    delivery_time = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.distance_km = calculate_distance(self.location, self.restaurant.location)
        self.total_quantity, price, self.total_price = calculate_totals(self)
        self.estimated_time, self.preparation_time, self.delivery_time = estimate_delivery(self)
        self.delivery_fee = 0
        self.total_price = price + self.delivery_fee
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    dish = models.ForeignKey('dishes.Dish', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f'{self.dish}'