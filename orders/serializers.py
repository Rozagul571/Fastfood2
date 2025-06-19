from rest_framework import serializers
from orders.models import Order, OrderItem
from restaurants.models import Restaurant
from dishes.models import Dish
from django.contrib.gis.geos import Point

class OrderItemSerializer(serializers.ModelSerializer):
    dish_id = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all(), source="dish", write_only=True)
    dish = serializers.CharField(source="dish.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ("id", "dish", "dish_id", "quantity")

class OrderSerializer(serializers.ModelSerializer):
    restaurant_id = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all(), source="restaurant", write_only=True)
    order_items = OrderItemSerializer(many=True)
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)

    class Meta:
        model = Order
        fields = (
            "id", "user", "restaurant_id", "order_items",
            "delivery_address", "latitude", "longitude", "location",
            "distance_km", "delivery_fee",
            "total_quantity", "total_price", "preparation_time", "delivery_time", "estimated_time"
        )
        read_only_fields = (
            "id", "user", "location", "distance_km", "delivery_fee",
            "total_quantity", "total_price", "preparation_time", "delivery_time", "estimated_time"
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["latitude"] = instance.location.y if instance.location else None
        data["longitude"] = instance.location.x if instance.location else None
        return data

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        lat = validated_data.pop('latitude')
        lon = validated_data.pop('longitude')
        validated_data['location'] = Point(lon, lat, srid=4326)
        validated_data['user'] = self.context['request'].user
        order = Order.objects.create(**validated_data)
        items = []
        for item_data in order_items_data:
            dish = item_data['dish']
            quantity = item_data['quantity']
            price = dish.price
            items.append(OrderItem(order=order, dish=dish, quantity=quantity, price=price))
        OrderItem.objects.bulk_create(items)
        order.save()
        return order

    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('order_items', None)
        lat = validated_data.pop('latitude', None)
        lon = validated_data.pop('longitude', None)
        if lat is not None and lon is not None:
            instance.location = Point(lon, lat, srid=4326)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if order_items_data:
            instance.order_items.all().delete()
            items = []
            for item_data in order_items_data:
                dish = item_data['dish']
                quantity = item_data['quantity']
                price = dish.price
                items.append(OrderItem(order=instance, dish=dish, quantity=quantity, price=price))
            OrderItem.objects.bulk_create(items)
        return instance

