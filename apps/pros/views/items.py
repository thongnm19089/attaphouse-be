from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ..models import Item
from ..serializers import ItemSerializer

class ItemViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = Item.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ItemSerializer

