from rest_framework import serializers
from dishes.models import Dish, Category

class CategorySerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),source="parent", write_only=True,required=False,allow_null=True)
    parent = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'parent', 'parent_id')

class DishSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source="category", write_only=True)
    is_available = serializers.BooleanField(read_only=True)

    class Meta:
        model = Dish
        fields = ('id', 'name', 'description', 'price', 'category', 'category_id', 'is_available', 'created_at')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        user = self.context['request'].user if 'request' in self.context else None
        if user and user.is_authenticated and user.role in ['admin', 'waiter']:
            rep['is_available'] = instance.is_available
        return rep