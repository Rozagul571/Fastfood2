from rest_framework import serializers
from restaurants.models import Restaurant
from django.contrib.gis.geos import Point

class RestaurantSerializer(serializers.ModelSerializer):
    latitude = serializers.FloatField(write_only=True, required=True)
    longitude = serializers.FloatField(write_only=True, required=True)
    location = serializers.HiddenField(default=None)

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'location', 'latitude', 'longitude', 'waiters')

    def validate(self, data):
        data['location'] = Point(data['longitude'], data['latitude'])
        return data

    def create(self, validated_data):
        validated_data.pop('latitude')
        validated_data.pop('longitude')
        return super().create(validated_data)

    def update(self, validated_data, instance):
        validated_data.pop('latitude')
        validated_data.pop('longitude')
        return super().update(instance, validated_data)