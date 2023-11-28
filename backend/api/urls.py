from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from .views import (
    CardViewSet,
    GroupViewSet,
    ShopEditViewSet,
    ShopViewSet,
    TokenDestroyView,
    UserViewSet,
)


app_name = 'api'

router = DefaultRouter()

router.register('users', UserViewSet)
router.register('cards', CardViewSet)
router.register('shops', ShopViewSet)
router.register('groups', GroupViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="OSDC API",
        default_version='v1',
        description="Документация для проекта OSDC",
        contact=openapi.Contact(email="admin@admin.ru"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('v1/shops/<int:pk>/', ShopEditViewSet.as_view(), name="shop-edit"),
    path('v1/', include(router.urls)),
    path('v1/auth/token/logout/', TokenDestroyView.as_view(), name="logout"),
    path('v1/auth/', include('djoser.urls.authtoken')),
    path(
        'docs/swagger/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    path(
        'docs/redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
]
