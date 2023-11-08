from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action

from core.models import Card, Group, Shop

from .serializers import CardSerializer, GroupSerializer, ShopSerializer

User = get_user_model()


class UserViewSet(UserViewSet):
    """Набор представлений для просмотра и редактирования
    пользовательских экземпляров."""
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @action(["get", "patch"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)


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
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
