from django.contrib import admin
from .models import (
    Color,
    Product,
    Brand,
)
# Register your models here.
admin.site.register(Color)
admin.site.register(Product)
admin.site.register(Brand)