from django.db import models
import uuid
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from ...products.models import Product
from .order import Order

class OrderDetails(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name="order_details", null=True)
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_details")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "order_details"
        ordering = ["-created_at"]