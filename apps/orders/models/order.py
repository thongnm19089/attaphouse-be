from django.db import models
import uuid
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from ...users.models import User

class Order(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="orders", null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "order"
        ordering = ["-created_at"]