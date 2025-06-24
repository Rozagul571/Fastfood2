from rest_framework import serializers
from restaurants.models import Restaurant
from django.contrib.gis.geos import Point
from users.models import User

class WaiterSerializer(serializers.Serializer):
    waiter_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='waiter'), source='id')  # QO‘SHILDI: Faqat waiter roli

    def validate_waiter_id(self, value):
        if not value.role == 'waiter':
            raise serializers.ValidationError("Use must be waiter")
        return value

class RestaurantCreateSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)
    location = serializers.HiddenField(default=None)

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'latitude', 'longitude', 'location')  # SAQLANDI: waiters yo‘q
        read_only_fields = ('id', 'location')


class RestaurantSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(source='location.y', read_only=True)
    longitude = serializers.FloatField(source='location.x', read_only=True)
    waiters = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'latitude', 'longitude', 'location', 'waiters')
        read_only_fields = ('id', 'latitude', 'longitude', 'location', 'waiters')