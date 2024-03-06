from django.db import models
import uuid
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

class Tag(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tag"
        constraints = [
            models.UniqueConstraint(
                fields=["name"], name="unique_tag_name"
            ),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return '{}'.format(self.name)