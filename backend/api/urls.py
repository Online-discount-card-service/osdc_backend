from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from .views import (
    CardViewSet,
    CustomTokenDestroyView,
    CustomUserViewSet,
    GroupViewSet,
    ShopViewSet,
)


DJOSER_METHODS_TO_EXCLUDE = (
    'user-reset-username',
    'user-reset-username-confirm',
    'user-set-password',
    'user-set-username',
)

app_name = 'api'

djoser_router = DefaultRouter()
djoser_router.register('users', CustomUserViewSet)
users_urls = [
    url_pattern for url_pattern in djoser_router.urls
    if url_pattern.name not in DJOSER_METHODS_TO_EXCLUDE
]

router = DefaultRouter()
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
    path(
        'v1/',
        include(users_urls)
    ),
    path(
        'v1/',
        include(router.urls)
    ),
    path(
        'v1/auth/token/logout/',
        CustomTokenDestroyView.as_view(),
        name='logout'
    ),
    path(
        'v1/auth/',
        include('djoser.urls.authtoken'),
    ),
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
