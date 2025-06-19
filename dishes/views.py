from rest_framework import viewsets
from dishes.models import Dish, Category
from dishes.serializers import DishSerializer, CategorySerializer
from users.permissions import RoleBasedPermission

class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [RoleBasedPermission]
    allowed_roles = ["admin", "waiter", "user"]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Dish.objects.none()
        if user.role in ['admin', 'waiter']:
            return Dish.objects.all()
        return Dish.objects.filter(is_available=True)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [RoleBasedPermission]
    allowed_roles = ["admin", "waiter", "user"]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Category.objects.none()
        return Category.objects.all()