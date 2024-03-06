from django.db import models
import uuid
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from apps.categories.models import Category
class Item(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="item"
    )
    name = models.CharField(max_length=225, blank = False, null = False)
    img = models.CharField(max_length=255, blank=False, null=False)
    detail = models.TextField(blank=False, null =False)
    price = models.FloatField(max_length= 64, blank=False , null= False)
    rating = models.FloatField(max_length=2, blank=False , null =False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "item" 
        ordering = ["-created_at"]

    def __str__(self):
        return '{}'.format(self.name)