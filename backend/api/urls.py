from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet, CardViewSet, ShopViewSet, GroupViewSet

app_name = 'api'

router = DefaultRouter()

router.register(
    'users',
    UserViewSet
)
router.register('cards', CardViewSet)
router.register('shops', ShopViewSet)
router.register('groups', GroupViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
