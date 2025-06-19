from rest_framework import viewsets
from restaurants.models import Restaurant
from restaurants.serializers import RestaurantSerializer
from users.permissions import RoleBasedPermission

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [RoleBasedPermission]
    allowed_roles = ["admin", "waiter", "user"]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Restaurant.objects.none()
        return Restaurant.objects.all()