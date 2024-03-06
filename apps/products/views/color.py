from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ..models import Color
from ..serializers import ColorSerializer

class ColorViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = Color.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ColorSerializer