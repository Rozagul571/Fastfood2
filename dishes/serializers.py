from rest_framework import serializers
from dishes.models import Dish, Category
from restaurants.models import Restaurant

class CategorySerializer(serializers.ModelSerializer):
    restaurant_id = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all(), source="restaurant", write_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'restaurant_id')


class DishSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)
    restaurant_id = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all(), source='restaurant', write_only=True)
    category = serializers.StringRelatedField(read_only=True)
    restaurant = serializers.StringRelatedField(read_only=True)
    price = serializers.FloatField()

    class Meta:
        model = Dish
        fields = ('id', 'name', 'description', 'price', 'category', 'category_id', 'restaurant', 'restaurant_id', 'is_available')
        read_only_fields = ('id', 'category', 'restaurant', 'is_available')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        user = self.context['request'].user if 'request' in self.context else None
        if user and user.is_authenticated and user.role in ['admin', 'waiter']:
            rep['is_available'] = instance.is_available
        return rep

    def validate(self, data):
        category = data['category']
        restaurant = data['restaurant']
        if category.restaurant != restaurant:
            raise serializers.ValidationError(f"{category.name} category {restaurant.name} isn't match")
        return data

    def create(self, validated_data):
        return Dish.objects.create(**validated_data)

