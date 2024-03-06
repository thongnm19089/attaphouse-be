from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from ..models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['deleted', 'is_superuser']

class UserReadOnlySerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    email = serializers.CharField(read_only=True)
    fullname = serializers.CharField(read_only=True)
    phone = serializers.CharField(read_only=True)
    avatar_url = serializers.FileField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    # role = serializers.UUIDField(read_only=True, source="role_id")
    created_at = serializers.DateTimeField(read_only=True)
    is_block = serializers.BooleanField(read_only=True)

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

class RegisterSerializer(serializers.Serializer):
    fullname = serializers.CharField(max_length=50, required=True)
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate_email(self, email):
        for account in User.objects.all():
            if(account.email == email):
                raise serializers.ValidationError(_("Email is existed"))