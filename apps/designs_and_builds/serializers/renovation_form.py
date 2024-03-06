from rest_framework import serializers
from ..models import RenovationForm
from ...uploads.serializers import FileSerializer

class RenovationFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = RenovationForm
        exclude = ['deleted']

class GetRenovationFormSerializer(serializers.ModelSerializer):
    floor_plan = FileSerializer()
    house_design = FileSerializer(many=True)
    class Meta:
        model = RenovationForm
        exclude = ['deleted']