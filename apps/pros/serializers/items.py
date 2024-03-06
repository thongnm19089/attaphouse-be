from rest_framework import serializers
from ..models import Item

class ItemSerializer(serializers.ModelSerializer):
    # class Meta:
    #     model = Item
    #     exclude = ['deleted']
    class Meta:
        model=Item
        a = Item.objects.first()
        id= a.category.id
        category_n= a.category.name
        #a=Item.objects.name()
        print(category_n)
        #fields=('category_n','name','img','detail','price','rating')