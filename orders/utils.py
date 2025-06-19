from decimal import Decimal
from django.db.models import Sum

def calculate_totals(order):
    result = order.order_items.aggregate(
        total_quantity=Sum('quantity'),
        total_price=Sum('price'),
    )
    quantity = result['total_quantity'] or 0
    price = result['total_price'] or Decimal(0)
    total = price + order.delivery_fee
    return quantity, price, total

def estimate_delivery(order):
    result = order.order_items.aggregate(total_quantity=Sum('quantity'))
    quantity = result['total_quantity'] or 0
    # 5 min / 4 dish = 75
    preparation = quantity * 75
    delivery = float(order.distance_km) * 180  # 3 min = 180 s
    total_time = preparation + delivery
    return int(total_time), int(preparation), int(delivery)

def calculate_distance(user_location, rest_location):
    if user_location and rest_location:
        return round(user_location.distance(rest_location) / 1000, 3) # 3 min 1km  un
    return 0