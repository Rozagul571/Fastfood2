from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView
from orders.filters import OrderFilter
from orders.models import Order
from orders.serializers import OrderSerializer
from fastfood.permissions import Permissions

class OrderListCreateView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [Permissions]
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_authenticated and user.role == 'user':
    #         return self.queryset.filter(user=user)
    #     if user.is_authenticated and user.role == 'waiter':
    #         return self.queryset.filter(restaurant__waiters=user)
    #     return self.queryset