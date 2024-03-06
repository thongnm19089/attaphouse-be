from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ..models import Order, OrderDetails

from ..serializers import OrderSerializer, OrderDetailsSerializer, GetOrderSerializer
from django.shortcuts import get_object_or_404
from core.mixins import GetSerializerClassMixin

class OrderViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = Order.objects.all()
    permission_classes = [AllowAny]
    serializer_class = OrderSerializer
    serializer_action_classes = {
        "retrieve": GetOrderSerializer,
    }
    def create(self, request, *args, **kwargs):
        order_details = request.data.get('order_details')
        if order_details:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            order = serializer.save()

            for od in order_details:
                od['order'] = order.id
                order_details_serializer = OrderDetailsSerializer(data=od)
                order_details_serializer.is_valid(raise_exception=True)
                order_details_serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"order_details": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        order_details = request.data.get('order_details')
        if order_details:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            for od in order_details:
                id = od.get('id', None)
                if id:
                    order_details_instance = get_object_or_404(OrderDetails, pk=id)
                    order_details_serializer = OrderDetailsSerializer(order_details_instance, data=od, partial=True)
                    order_details_serializer.is_valid(raise_exception=True)
                    order_details_serializer.save()
                else:
                    od['order'] = self.kwargs['pk']
                    order_details_serializer = OrderDetailsSerializer(data=od)
                    order_details_serializer.is_valid(raise_exception=True)
                    order_details_serializer.save()
            deletes = request.data.get('deleted_order_details', None)
            if deletes:
                for d in deletes:
                    order_details = get_object_or_404(OrderDetails, pk=d)
                    order_details.delete()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"order_details": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)