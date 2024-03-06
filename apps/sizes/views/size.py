from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ..models import Size
from ..serializers import SizeSerializer

class SizeViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = Size.objects.all()
    permission_classes = [AllowAny]
    serializer_class = SizeSerializer