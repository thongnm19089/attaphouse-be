import uuid
import jwt
from datetime import datetime, timedelta
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.db.models import Q
from safedelete.models import SafeDeleteMixin, SOFT_DELETE_CASCADE
from .user_manager import CustomUserManager
from .role import Role

class User(SafeDeleteMixin, AbstractBaseUser):
    _safedelete_policy = SOFT_DELETE_CASCADE
    USERNAME_FIELD = "email"
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fullname = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, blank=True, null=True, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    avatar_url = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_block = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="users",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    object = CustomUserManager()
    
    @property
    def is_staff(self):
        return self.is_superuser

    @property
    def token(self):
        return self._generate_jwt_token()

    def clean(self):
        super().clean()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    class Meta:
        db_table = "user"
        constraints = [
            models.UniqueConstraint(
                fields=["phone"],
                name="unique_user_phone",
                condition=Q(deleted__isnull=True),
            ),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return (
            self.email
            if self.email
            else "{}-{}".format(self.fullname, self.phone)
        )

    def _generate_jwt_token(self):
        iat = datetime.now()
        exp = iat + timedelta(days=60)
        
        payload = {
            "id": str(self.id),
            "fullname": self.fullname,
            "phone": self.phone,
            "exp": exp,
            "iat": iat,
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        return token.decode('utf-8')