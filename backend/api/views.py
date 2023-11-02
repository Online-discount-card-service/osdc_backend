from djoser.views import UserViewSet
from rest_framework.permissions import (IsAuthenticatedOrReadOnly)
from rest_framework import viewsets
from django.contrib.auth import get_user_model

from core.models import Card, Shop, Group
from .serializers import CardSerializer, ShopSerializer, GroupSerializer

User = get_user_model()


class UserViewSet(UserViewSet):
    """Набор представлений для просмотра и редактирования
    пользовательских экземпляров."""
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CardViewSet(viewsets.ModelViewSet):
    """"""
    queryset = Card.objects.all()
    serializer_class = CardSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ShopViewSet(viewsets.ReadOnlyModelViewSet):
    """"""
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """"""
    queryset = Shop.objects.all()
    serializer_class = GroupSerializer
