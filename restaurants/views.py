from rest_framework import viewsets
from restaurants.models import Restaurant
from restaurants.serializers import RestaurantSerializer
from fastfood.permissions import Permissions

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [Permissions]