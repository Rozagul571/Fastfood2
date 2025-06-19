from django_filters import rest_framework as filters
from orders.models import Order

class OrderFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=Order.OrderStatus.choices)
    user = filters.NumberFilter(field_name='user__id')
    restaurant = filters.NumberFilter(field_name='restaurant__id')
    min_total_price = filters.NumberFilter(field_name='total_price', lookup_expr='gte')
    max_total_price = filters.NumberFilter(field_name='total_price', lookup_expr='lte')

    class Meta:
        model = Order
        fields = ['status', 'user', 'restaurant', 'min_total_price', 'max_total_price']