from decimal import Decimal
from django.db.models import Sum

def calculate_distance(user_location, rest_location):
    if user_location and rest_location:
        distance = user_location.distance(rest_location) / 1000
        return round(distance, 3) if distance > 0 else None
    return None

def calculate_totals(order):
    result = order.order_items.aggregate(
        total_quantity=Sum('quantity'),
        total_price=Sum('price')
    )
    quantity = result['total_quantity'] or 0
    price = result['total_price'] or Decimal('0.00')
    total = price + (order.delivery_fee or Decimal('0.00'))
    return quantity, price, total

def estimate_delivery(order):
    result = order.order_items.aggregate(total_quantity=Sum('quantity'))
    quantity = result['total_quantity'] or 0
    preparation = quantity * 75
    delivery = float(order.distance_km or 0) * 180
    total_time = preparation + delivery
    return int(total_time), int(preparation), int(delivery)