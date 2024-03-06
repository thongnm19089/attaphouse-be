from django.db import models
import uuid
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from ...uploads.models import File

class RenovationForm(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    type_property = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=15)
    property_location = models.CharField(max_length=150, blank=True)
    floor_plan = models.ForeignKey(File, on_delete=models.SET_NULL, related_name="floor_plan_renovation_form", null=True)
    house_design = models.ManyToManyField(File, blank=True, related_name="house_design_renovation_form")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "renovation_form"
        ordering = ["-created_at"]

    def __str__(self):
        return '{}'.format(self.name)


