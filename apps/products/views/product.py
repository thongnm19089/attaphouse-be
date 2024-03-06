from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from ..models import Product
from ..serializers import ProductSerializer, GetProductSerializer
from datetime import datetime, timedelta
from django.db.models import Sum
from django.db.models import Q
from core.mixins import GetSerializerClassMixin
from ...uploads.serializers import FileSerializer
from django.shortcuts import get_object_or_404
from ...uploads.models import File
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.parsers import MultiPartParser

def checkStock(cart_items):
    for ci in cart_items:
        product_id = ci['product']
        quantity = Product.objects.filter(Q(id=product_id) & Q(quantity__gt=ci['quantity']))
        if quantity.exists() == False:
            product = get_object_or_404(Product, pk=product_id)
            return product.name + ' out of stock'
    return True

class ProductViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = Product.objects.all()
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    serializer_action_classes = {
        "retrieve": GetProductSerializer,
        "list": GetProductSerializer,
    }
    parser_classes = (MultiPartParser,)
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name="image", in_=openapi.IN_FORM, type=openapi.TYPE_FILE,description="Document"),
            openapi.Parameter(name="sub_image", in_=openapi.IN_FORM, type=openapi.TYPE_FILE,description="Document")
        ],
    )
    def create(self, request, *args, **kwargs):
        image = self.request.FILES.getlist('image', None)
        sub_file = self.request.FILES.getlist('sub_image', None)
        if image:
            data_image = {
                'name': 'products',
                'file': image[0]
            }
            image_serializer = FileSerializer(data=data_image)
            image_serializer.is_valid(raise_exception=True)
            file = image_serializer.save()
            request.data['image'] = file.id
        if sub_file:
            del request.data['sub_image']
        serializer = self.get_serializer(data=request.data) 
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        list_sub_image = []
        for sf in sub_file:
            data_sub_image = {
                'name': 'products',
                'file': sf
            }
            sub_image_serializer = FileSerializer(data=data_sub_image)
            sub_image_serializer.is_valid(raise_exception=True)
            sub_image = sub_image_serializer.save()
            list_sub_image.append(sub_image.id)
        product.sub_image.set(list_sub_image)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name="image", in_=openapi.IN_FORM, type=openapi.TYPE_FILE,description="Document"),
            openapi.Parameter(name="sub_image", in_=openapi.IN_FORM, type=openapi.TYPE_FILE,description="Document")
        ],
    )
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        image = self.request.FILES.getlist('image', None)
        sub_file = self.request.FILES.getlist('sub_image', None)
        if image:
            instance.image.delete()
            data_image = {
                'name': 'products',
                'file': image[0]
            }
            image_serializer = FileSerializer(data=data_image)
            image_serializer.is_valid(raise_exception=True)
            file = image_serializer.save()
            request.data['image'] = file.id
        if sub_file:
            del request.data['sub_image']
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        list_sub_image = []
        for old_sf in instance.sub_image.all():
           list_sub_image.append(old_sf.id)
        for sf in sub_file:
            data_sub_image = {
                'name': 'products',
                'file': sf
            }
            sub_image_serializer = FileSerializer(data=data_sub_image)
            sub_image_serializer.is_valid(raise_exception=True)
            sub_image = sub_image_serializer.save()
            list_sub_image.append(sub_image.id)
        instance.sub_image.set(list_sub_image)
        deletes = request.data.get('deleted_sub_image', None)
        if deletes:
            for d in deletes:
                order_details = get_object_or_404(File, pk=d)
                order_details.delete()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        brand = self.request.GET.get('brand_id')
        if brand is not None:
            queryset = queryset.filter(brand=brand)
        
        category = self.request.GET.get('category_id')
        if category is not None:
            queryset = queryset.filter(sub_category__category=category)
        
        sub_category = self.request.GET.get('sub_category_id')
        if sub_category is not None:
            queryset = queryset.filter(sub_category=sub_category)

        view = self.request.GET.get('view')
        if view is not None:
            if view == 'best_selling':
                queryset = queryset.filter(order_details__created_at__lte=datetime.today(), order_details__created_at__gt=datetime.today()-timedelta(days=7)).annotate(quantity_sum=Sum('order_details__quantity')).order_by('-quantity_sum')[:8]
            elif view == 'everyday_deals':
                print(datetime.today())
                queryset = queryset.filter(Q(promotions__start_day__lte=datetime.today()) & Q(promotions__end_day__gt=datetime.today())).order_by('-promotions__discount')[:8]

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)