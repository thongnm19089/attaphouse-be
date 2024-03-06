from django.db import models
import uuid
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

class Color(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "color"
        constraints = [
            models.UniqueConstraint(
                fields=["name"], name="unique_color_name"
            ),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return '{}'.format(self.name)