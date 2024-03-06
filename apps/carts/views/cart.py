from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import transaction
from apps.carts.models import cart_item
from apps.products.models import product
from apps.products.models.product import Product
from ..models import Cart, CartItem
from ..serializers import CartSerializer, CartItemSerializer, GetCartSerializer
from django.shortcuts import get_object_or_404
from ...products.views import checkStock
from core.mixins import GetSerializerClassMixin

class CartViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = Cart.objects.all()
    permission_classes = [AllowAny]
    serializer_class = CartSerializer
    serializer_action_classes = {
        "retrieve": GetCartSerializer,
        "list": GetCartSerializer,
    }

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        cart_items = request.data.get('cart_items', None)
        if cart_items:
            check = checkStock(cart_items)
            if check == True:
                for ci in cart_items:
                    id = ci.get('id', None)
                    if id:
                        order_details_instance = get_object_or_404(CartItem, pk=id)
                        order_details_serializer = CartItemSerializer(order_details_instance, data=ci, partial=True)
                        order_details_serializer.is_valid(raise_exception=True)
                        order_details_serializer.save()
                    else:
                        ci['cart'] = self.kwargs['pk']
                        order_details_serializer = CartItemSerializer(data=ci)
                        order_details_serializer.is_valid(raise_exception=True)
                        order_details_serializer.save()
            else:
                return Response(check, status=status.HTTP_200_OK)
        deletes = request.data.get('deleted_cart_items', None)
        if deletes:
            for d in deletes:
                cart_item = get_object_or_404(CartItem, pk=d)
                cart_item.delete()
        return Response(serializer.data, status=status.HTTP_200_OK)