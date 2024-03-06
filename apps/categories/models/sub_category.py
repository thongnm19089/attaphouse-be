from django.db import models
import uuid
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from .category import Category


class SubCategory(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=50, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="sub_categories")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sub_category"
        constraints = [
            models.UniqueConstraint(
                fields=["name"], name="unique_sub_category_name"
            ),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return '{}'.format(self.name)