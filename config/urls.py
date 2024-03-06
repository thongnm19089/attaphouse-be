"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from apps.carts.views.cart import CartViewSet

swagger_info = openapi.Info(
    title="AttapHouse API",
    default_version="v1",
    description="""AttapHouse project.""",
    contact=openapi.Contact(email="anhnguyenbinhminh2302@gmail.com"),
    license=openapi.License(name="Private")
)

schema_view = get_schema_view(
    info=swagger_info,
    public=True,
    permission_classes=(permissions.AllowAny,),
)

api_router = SimpleRouter(trailing_slash=False)

from apps.users.views import (
    UserViewSet
)

from apps.categories.views import (
    CategoryViewSet,
    SubCategoryViewSet
)

from apps.products.views import (
    ColorViewSet,
    ProductViewSet,
    BrandViewSet,
)

from apps.orders.views import (
    OrderViewSet,
)

from apps.promotions.views import (
    PromotionViewSet,
)

from apps.designs_and_builds.views import (
    RenovationFormViewSet,
)

from apps.carts.views import (
    CartViewSet,
)

from apps.tags.views import (
    TagViewSet,
)

from apps.sizes.views import (
    SizeViewSet,
)
from apps.orders.views import (
    AddressViewSet,
)
from apps.pros.views import (
    ItemViewSet
)
api_router.register('users', UserViewSet, basename='users')
api_router.register('categories', CategoryViewSet, basename='categories')
api_router.register('sub_categories', SubCategoryViewSet, basename='sub_categories')
api_router.register('colors', ColorViewSet, basename='colors')
api_router.register('products', ProductViewSet, basename='products')
api_router.register('brands', BrandViewSet, basename='brands')
api_router.register('orders', OrderViewSet, basename='orders')
api_router.register('promotions', PromotionViewSet, basename='promotions')
api_router.register('renovation_forms', RenovationFormViewSet, basename='renovation_forms')
api_router.register('carts', CartViewSet, basename='carts')
api_router.register('tags', TagViewSet, basename='tags')
api_router.register('sizes', SizeViewSet, basename='sizes')
api_router.register('address', AddressViewSet, basename='address')
api_router.register('item', ItemViewSet, basename='item')

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'api/v1/', include(api_router.urls)) 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns.extend([
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
])