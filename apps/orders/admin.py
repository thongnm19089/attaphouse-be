from django.contrib import admin
from .models import (
    Order,
    OrderDetails,
    Address
)
# Register your models here.
admin.site.register(Order)
admin.site.register(OrderDetails)
admin.site.register(Address)