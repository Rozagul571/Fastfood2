from django.urls import path
from orders.views import OrderListCreateView, OrderItemListCreateView

urlpatterns = [
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('order-items/', OrderItemListCreateView.as_view(), name='order-item-list-create'),
]