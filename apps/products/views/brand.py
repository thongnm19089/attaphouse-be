from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ..models import Brand
from ..serializers import BrandSerializer

class BrandViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = Brand.objects.all()
    permission_classes = [AllowAny]
    serializer_class = BrandSerializer