from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Card, Group, Shop, UserCards

from .permissions import IsCardsUser
from .serializers import (
    CardEditSerializer,
    CardSerializer,
    CardShopCreateSerializer,
    CardsListSerializer,
    GroupSerializer,
    ShopSerializer,
)


User = get_user_model()


class UserViewSet(UserViewSet):
    """Вьюсет для данных пользователя. Возможны просмотр и редактирование."""

    permission_classes = (IsAuthenticated,)

    @action(["get", "patch"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)


class CardViewSet(viewsets.ModelViewSet):
    """Вьюсет для класса Карт."""

    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = (IsCardsUser,)

    def get_serializer_class(self):
        if self.action == 'list':
            return CardsListSerializer
        elif self.action == 'create':
            return CardEditSerializer
        return CardSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return
        if self.action == 'list':
            return (
                self.request.user.cards.
                select_related('card', 'card__shop').
                prefetch_related('card__shop__group')
            )
        else:
            return (
                Card.objects.filter(users=self.request.user).
                select_related('shop').
                prefetch_related('shop__group')
            )

    def perform_create(self, serializer):
        card = serializer.save()

        user = self.request.user
        UserCards.objects.create(
            user=user,
            card=card,
            owner=True,
            favourite=False,
        )

    def perform_destroy(self, instance):
        id = instance.id
        user = self.request.user
        user_card = UserCards.objects.get(user=user, card__id=id)
        if user_card.owner:
            card = Card.objects.get(id=id)
            card.delete()
        user_card.delete()

    @swagger_auto_schema(
        responses={200: CardsListSerializer(many=True)},
        operation_summary='Список карт текущего пользователя',
        operation_description=(
            'Проверяет авторизацию пользователя'
            'и выдает список его карт.'
        )
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={200: CardSerializer()},
        operation_summary='Данные конкретной карты',
        operation_description=(
            'Проверяет авторизацию пользователя,'
            'выдает данные карты, если она принадлежит '
            'пользователю.Иначе 404.'
        )
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=CardEditSerializer(),
        responses={201: CardEditSerializer()},
        operation_summary='Добавление новой карты',
        operation_description='''
            Создает новую карту и добавляет в список пользователя. \n
            Необходимо указать номер карты и/или штрих-кода. \n
            Поле image - string(binary) не показано в документации,
            но ожидается.
            '''
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=CardEditSerializer(),
        responses={200: CardEditSerializer()},
        operation_summary='Редактирование карты',
        operation_description='''
            Редактирует карту. \n
            Необходимо указать номер карты и/или штрих-кода. \n
            Поле image - string(binary) не показано в документации,
            но ожидается.
            '''
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=CardEditSerializer(),
        responses={200: CardEditSerializer()},
        operation_summary='Частичное редактирование карты',
        operation_description='''
            Частично редактирует карту. \n
            Необходимо указать номер карты и/или штрих-кода. \n
            Поле image - string(binary) не показано в документации,
            но ожидается.
        '''
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={204: None},
        operation_summary='Удаление карты',
        operation_description=(
            'Удаляет все данные о карте.')
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, url_path='favorite')
    def favorite(self, request, *args, **kwargs):
        """Возвращает список избранных карт."""

        favorite_cards = (
            self.request.user.cards.
            select_related('card', 'card__shop').
            prefetch_related('card__shop__group')
        ).filter(favourite=True)
        serializer = CardsListSerializer(favorite_cards, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'], url_path='new-shop',)
    def create_with_new_shop(self, request):
        user = self.request.user
        serializer = CardShopCreateSerializer(data=request.data)
        if serializer.is_valid():
            card = serializer.save()
            UserCards.objects.create(
                user=user,
                card=card,
                owner=True,
                favourite=False,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShopViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для отображения единично и списком Магазинов."""

    queryset = Shop.objects.filter(validation=True)
    serializer_class = ShopSerializer
    permission_classes = (AllowAny,)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для отображения единично и списком Категорий."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AllowAny,)


class CreateDestroyFavViewSet(APIView):
    """Вью для удаления и добавления карты в избранное."""

    def post(self, request, id):
        user = request.user
        user_card = get_object_or_404(UserCards, user=user, card__id=id)
        if user_card.favourite:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            user_card.favourite = True
            user_card.save()
            card = UserCards.objects.get(user=user, card__id=id)
            serializer = CardsListSerializer(card)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        user_card = get_object_or_404(UserCards, user=user, card__id=id)
        if not user_card.favourite:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            user_card.favourite = False
            user_card.save()
            card = UserCards.objects.get(user=user, card__id=id)
            serializer = CardsListSerializer(card)
            return Response(serializer.data, status=status.HTTP_200_OK)
