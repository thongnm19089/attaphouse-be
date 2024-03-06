from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ..models import RenovationForm
from ..serializers import RenovationFormSerializer, GetRenovationFormSerializer
from core.mixins import GetSerializerClassMixin
from ...uploads.serializers import FileSerializer

class RenovationFormViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = RenovationForm.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RenovationFormSerializer
    serializer_action_classes = {
        "retrieve": GetRenovationFormSerializer,
        "list": GetRenovationFormSerializer,
    }

    def create(self, request, *args, **kwargs):
        floor_plan = self.request.FILES.getlist('floor_plan', None)
        if floor_plan:
            data_floor_plan = {
                'name': 'renovation_forms',
                'file': floor_plan[0]
            }
            floor_plan_serializer = FileSerializer(data=data_floor_plan)
            floor_plan_serializer.is_valid(raise_exception=True)
            file = floor_plan_serializer.save()
            request.data['floor_plan'] = file.id
        serializer = self.get_serializer(data=request.data) 
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)