from rest_framework import serializers

from apps.products.models import product
from ..models import CartItem
from ...products.serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        exclude = ['deleted']

class GetCartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    
    class Meta:
        model = CartItem
        exclude = ['deleted']