from django.contrib.auth.base_user import BaseUserManager
from safedelete.managers import SafeDeleteManager


class CustomUserManager(SafeDeleteManager, BaseUserManager):
    def create(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.is_superuser = True
        user.save(using=self._db)
        return user