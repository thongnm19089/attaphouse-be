from rest_framework import serializers

from apps.orders.models import order_details
from ..models import Order, OrderDetails

class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetails
        exclude = ['deleted']

class OrderSerializer(serializers.ModelSerializer):
    deleted_order_details = serializers.ListField(child=serializers.UUIDField(), required=False, allow_null=True)
    class Meta:
        model = Order
        exclude = ['deleted']

class GetOrderSerializer(serializers.ModelSerializer):
    order_details = OrderDetailsSerializer(many=True)
    class Meta:
        model = Order
        exclude = ['deleted']