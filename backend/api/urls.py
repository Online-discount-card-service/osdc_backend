from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import UserViewSet

app_name = 'api'

router = DefaultRouter()

router.register(
    'users',
    UserViewSet
)

urlpatterns = [
    path('', include(router.urls)),
]
