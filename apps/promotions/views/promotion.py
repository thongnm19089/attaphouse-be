from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ..models import Promotion
from ..serializers import PromotionSerializer

class PromotionViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = Promotion.objects.all()
    permission_classes = [AllowAny]
    serializer_class = PromotionSerializer