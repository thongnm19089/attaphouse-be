from django.db import models
import uuid
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from ...users.models import User
class Address(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="shipping_address")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    address = models.TextField(null=False, blank=False)
    default = models.BooleanField(null=True, blank=True, default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "address" 
        ordering = ["-created_at"]

    def __str__(self):
        return '{}-{}'.format(self.first_name, self.last_name)