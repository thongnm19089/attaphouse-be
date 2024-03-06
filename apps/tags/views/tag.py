from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ..models import Tag
from ..serializers import TagSerializer

class TagViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = Tag.objects.all()
    permission_classes = [AllowAny]
    serializer_class = TagSerializer