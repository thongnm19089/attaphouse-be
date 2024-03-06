from django.db import models
import uuid

def upload_to(instance, filename):
    return '/'.join(['images', str(instance.name), filename])

class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to=upload_to, blank=True, null=True)

    class Meta:
        db_table = "image"