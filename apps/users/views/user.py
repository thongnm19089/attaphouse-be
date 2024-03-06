from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status, exceptions
from django.db import transaction
from django.db import IntegrityError
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from core.mixins import GetSerializerClassMixin
from ..models import User
from apps.users.serializers import (
    UserSerializer,
    UserReadOnlySerializer,
    LoginSerializer,
    RegisterSerializer
)
from rest_framework.permissions import IsAuthenticated, AllowAny
from core.permissions import UserRolePermission
class UserViewSet(GetSerializerClassMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    serializer_action_classes = {
        "list": UserReadOnlySerializer,
        "retrieve": UserReadOnlySerializer,
    }
    permission_classes = [IsAuthenticated, UserRolePermission]

    def get_queryset(self):
        queryset = self.queryset.all()
        if not self.request.user.is_superuser:
            queryset = queryset.exclude(is_superuser=True)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
        except IntegrityError:
            return Response({'detail': 'User with that email already exists.'},status=status.HTTP_409_CONFLICT)
            
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            self.object.set_password(serializer.data.get("password"))
            self.object.save()

        return Response({'message': 'User updated successfully.'}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Login",
        request_body=LoginSerializer,
        responses={200: LoginSerializer},
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="login",
        url_name="login",
        permission_classes=[],
        pagination_class=None,
    )
    def login(self, request, *args, **kwargs):   
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            try:
                user = authenticate(email=email, password=password)
            except exceptions.NotFound:
                raise APIException(
                    _("Email or password is wrong"),
                    status.HTTP_404_NOT_FOUND,
                )
            except:
                raise APIException(_("Invalid token"), status.HTTP_400_BAD_REQUEST)
            if not user:
                raise APIException(
                    _("User with email {email} not found").format(email=email),
                    status.HTTP_404_NOT_FOUND,
                )
           
            serialized_user = UserSerializer(user).data
            token = user.token
            data = {
                "token": token,
                "user": {
                    "id": serialized_user["id"],
                    "name": serialized_user["fullname"],
                }
            }
            return Response(data=data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Register",
        request_body=RegisterSerializer,
        responses={200: RegisterSerializer},
    )
    @action(
        methods=["POST"],
        detail=False,
        url_path="register",
        url_name="register",
        permission_classes = [AllowAny]
    )
    def register(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
       
        try:
            user = request.user
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                intance = serializer.save()
                intance.set_password(data['password'])
                intance.save()

        except Exception as e:
            raise APIException(str(e), status.HTTP_500_INTERNAL_SERVER_ERROR)

        token = intance.token
        data = {"token": token}
        return Response(data=data, status=status.HTTP_200_OK)