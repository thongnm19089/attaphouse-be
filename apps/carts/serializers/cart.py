from re import I
# from typing_extensions import Required
from rest_framework import serializers

from ..models import Cart
from .cart_item import GetCartItemSerializer

class CartItemWriteSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=False)
    product = serializers.UUIDField(required=False)
    quantity = serializers.IntegerField(required=False, min_value=1, default=1)

class CartSerializer(serializers.ModelSerializer):
    deleted_cart_items = serializers.ListField(child=serializers.UUIDField(), required=False, allow_null=True)
    cart_items = CartItemWriteSerializer(many=True, required=False, read_only=True)
    
    class Meta:
        model = Cart
        exclude = ['deleted']

class GetCartSerializer(serializers.ModelSerializer):
    cart_items = GetCartItemSerializer(many=True)
    
    class Meta:
        model = Cart
        exclude = ['deleted']