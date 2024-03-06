from rest_framework import serializers
from ..models import Product
from ...uploads.serializers import FileSerializer

class ProductSerializer(serializers.ModelSerializer):
    deleted_sub_image = serializers.ListField(child=serializers.UUIDField(), required=False, allow_null=True)
    class Meta:
        model = Product
        exclude = ['deleted']

class GetProductSerializer(serializers.ModelSerializer):
    image = FileSerializer()
    sub_image = FileSerializer(many=True)
    class Meta:
        model = Product
        exclude = ['deleted']