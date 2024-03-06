from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Q
from ..models import Address
from ..serializers import AddressSerializer

class AddressViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = Address.objects.all()
    permission_classes = [AllowAny]
    serializer_class = AddressSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        default = request.data.get('default')
        if (default is not None) & (default == True):
            user_id = request.user
            if user_id:
                updated_default = []
                address = Address.objects.filter(Q(user=user_id) & Q(default=True))
                for ad in address:
                    ad.default = False
                    updated_default.append(ad)

                Address.objects.bulk_update(updated_default, ['default'])
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request):
        user = request.user
        id = user.id
        queryset = Address.objects.filter(user_id = id)
        serializer = AddressSerializer(queryset, many=True)
        return Response(serializer.data)