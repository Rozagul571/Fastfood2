from rest_framework import serializers
from orders.models import Order, OrderItem
from dishes.models import Dish
from restaurants.models import Restaurant
from django.contrib.gis.geos import Point
from orders.utils import calculate_totals, estimate_delivery, calculate_distance
from decimal import Decimal

class OrderItemSerializer(serializers.ModelSerializer):
    dish_id = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all(), source="dish", write_only=True)
    dish = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'dish', 'dish_id', 'quantity', 'price')
        read_only_fields = ('id', 'price')

    def create(self, validated_data):
        dish = validated_data['dish']
        validated_data['price'] = dish.price
        return super().create(validated_data)

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)
    restaurant_id = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all(), source="restaurant", write_only=True)
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)
    location = serializers.HiddenField(default=None)
    distance_km = serializers.FloatField(read_only=True, allow_null=True)
    delivery_fee = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True, allow_null=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    preparation_time = serializers.IntegerField(read_only=True)
    delivery_time = serializers.IntegerField(read_only=True)
    estimated_time = serializers.IntegerField(read_only=True)
    delivery_address = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        fields = (
            'id', 'user', 'restaurant_id', 'status', 'delivery_address', 'location',
            'latitude', 'longitude', 'distance_km', 'delivery_fee',  'preparation_time', 'delivery_time', 'estimated_time',
            'order_items', 'total_price', 'created_at', 'updated_at'
        )
        read_only_fields = (
            'id', 'user', 'status', 'delivery_address', 'location', 'distance_km',
            'delivery_fee','preparation_time', 'delivery_time',
            'estimated_time', 'total_price',  'created_at', 'updated_at'
        )

    def validate(self, data):
        restaurant = data['restaurant']
        latitude = data['latitude']
        longitude = data['longitude']
        order_items = data['order_items']

        # for item in order_items:
        #     dish = item['dish']
        #     if dish.restaurant != restaurant:
        #         raise serializers.ValidationError(f"{dish.name} dish {restaurant.name} doesn't match")

        data['location'] = Point(longitude, latitude)
        data['delivery_address'] = f"latitude: {latitude}, longitude: {longitude}"
        return data

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        restaurant = validated_data['restaurant']
        user = self.context['request'].user
        location = validated_data['location']
        delivery_address = validated_data['delivery_address']
        distance_km = calculate_distance(location, restaurant.location)
        if distance_km is None:
            distance_km = None
            delivery_fee = None
        else:
            delivery_fee = Decimal(str(distance_km * 5000)).quantize(Decimal('0.01'))


        order = Order.objects.create(user=user,restaurant=restaurant, delivery_address=delivery_address,location=location,
            distance_km=distance_km, delivery_fee=delivery_fee)

        order_items = [
            OrderItem(order=order, dish=item_data['dish'], quantity=item_data['quantity'],
                price=item_data['dish'].price)
            for item_data in order_items_data
        ]
        OrderItem.objects.bulk_create(order_items)

        total_time, preparation, delivery = estimate_delivery(order)
        quantity, price, total = calculate_totals(order)

        order.preparation_time = preparation
        order.delivery_time = delivery
        order.estimated_time = total_time
        order.total_price = total
        order.save()

        return order

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        user = self.context['request'].user
        if user.role != 'admin':
            return {
                'id': rep['id'],
                'restaurant_id': rep['restaurant_id'],
                'delivery_address': rep['delivery_address'],
                'total_price': rep['total_price'],
                'estimated_time': rep['estimated_time'],
                'order_items': rep['order_items'],
                'created_at': rep['created_at']
            }
        return rep