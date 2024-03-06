import uuid
from enum import Enum

from django.db import models
from django.utils.translation import gettext_lazy as _
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE

class RoleName(Enum):
    HOMEOWNER = 'Homeowner'
    CONTRACTOR = 'Contractor'
    SERVICE_PROVIDER = 'Service Provider'
    MERCHANT = 'Merchant'

class Role(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "role"
        constraints = [
            models.UniqueConstraint(
                fields=["name"], name="unique_role_name"
            ),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return '{}'.format(self.name)

    @property
    def is_homeowner(self):
        return self.name == RoleName.HOMEOWNER.value

    @property
    def is_contractor(self):
        return self.name == RoleName.CONTRACTOR.value

    @property
    def is_service_provider(self):
        return self.name == RoleName.SERVICE_PROVIDER.value

    @property
    def is_merchant(self):
        return self.name == RoleName.MERCHANT.value