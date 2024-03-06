from django.db import models
import uuid
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from ...users.models import User

class Cart(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cart"
        ordering = ["-created_at"]