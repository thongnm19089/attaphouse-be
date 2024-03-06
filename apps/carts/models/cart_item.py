from django.db import models
import uuid
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from ...products.models import Product
from .cart import Cart

class CartItem(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.IntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cart_item"
        ordering = ["-created_at"]