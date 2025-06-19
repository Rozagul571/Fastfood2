from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer, OrderItemSerializer
from orders.filters import OrderFilter
from users.permissions import RoleBasedPermission
from django_filters.rest_framework import DjangoFilterBackend

class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all().select_related('user', 'restaurant').prefetch_related('order_items__dish')
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter
    # authentication_classes = (JWTAuthentication,)
    # permission_classes = [AllowAny]
    permission_classes = [RoleBasedPermission]

    allowed_roles = ["admin", "waiter", "user"]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Order.objects.none()
        if user.role == 'admin':
            return self.queryset
        elif user.role == 'waiter':
            return self.queryset.filter(restaurant__waiters=user)
        else:
            return self.queryset.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderItemListCreateView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.select_related('order', 'dish')
    serializer_class = OrderItemSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [RoleBasedPermission]
    # allowed_roles = ["admin", "waiter"]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return OrderItem.objects.none()
        if user.role == 'admin':
            return self.queryset
        elif user.role == 'waiter':
            return self.queryset.filter(order__restaurant__waiters=user)
        else:
            return OrderItem.objects.none()

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.role == 'admin':
    #         return self.queryset
    #     elif user.role == 'waiter':
    #         return self.queryset.filter(restaurant__waiters=user)
    #     else:
    #         return self.queryset.filter(user=user)

