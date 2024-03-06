from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ..models import SubCategory
from ..serializers import SubCategorySerializer

class SubCategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = SubCategory.objects.all()
    permission_classes = [AllowAny]
    serializer_class = SubCategorySerializer