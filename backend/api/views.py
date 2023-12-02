from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.permissions import CurrentUserOrAdmin
from djoser.views import TokenDestroyView, UserViewSet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core.models import Card, Group, Shop, UserCards
from users.tokens import custom_token_generator

from .exceptions import StatisticsError
from .permissions import IsCardsUser, IsShopCreatorOrReadOnly
from .serializers import (
    CardEditSerializer,
    CardSerializer,
    CardShopCreateSerializer,
    CardsListSerializer,
    GroupSerializer,
    ShopCreateSerializer,
    ShopSerializer,
    StatisticsSerializer,
)


User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Эндпоинт для просмотра и управления пользователями."""

    token_generator = custom_token_generator
    permission_classes = (CurrentUserOrAdmin,)

    @action(["get", "patch"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)


class CustomTokenDestroyView(TokenDestroyView):
    """Эндпоинт для выхода из учетной записи."""

    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            {'message': 'Вы успешно вышли из учетной записи.'},
            status=status.HTTP_200_OK
        )


class CardViewSet(viewsets.ModelViewSet):
    """Вьюсет для класса Карт."""

    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = (IsCardsUser,)

    def get_serializer_class(self):
        if self.action == 'list':
            return CardsListSerializer
        elif self.action in ('create', 'update', 'partial_update'):
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
            Создает новую карту и добавляет в список пользователя,
            назначает его владельцем по умолчанию.. \n
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
        operation_description='''
            Если пользователь является владельцем карты,
            удаляет все данные о карте. \n
            Если не является, удаляет карту из списка пользователя. \n
        '''
    )
    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            {'message': 'Карта успешно удалена.'},
            status=status.HTTP_200_OK
        )

    @swagger_auto_schema(
        request_body=CardShopCreateSerializer(),
        responses={201: CardShopCreateSerializer()},
        operation_summary='Добавление новой карты и магазина',
        operation_description='''
            Создает новую карту и новый магазин,
            добавляет карту в список пользователя,
            назначает его владельцем. \n
            Необходимо указать номер карты и/или штрих-кода. \n
            Поле image - string(binary) не показано в документации,
            но ожидается.
            '''
    )
    @action(
        detail=False,
        methods=['POST'],
        url_path='new-shop',
        name='new-shop',
    )
    def create_with_new_shop(self, request):
        user = self.request.user
        serializer = CardShopCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            card = serializer.save()
            UserCards.objects.create(
                user=user,
                card=card,
                owner=True,
                favourite=False,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={200: CardsListSerializer(many=True)},
        operation_summary='Список избранных карт текущего пользователя',
        operation_description=(
            'Проверяет авторизацию пользователя'
            'и выдает список его избранных карт.'
        )
    )
    @action(detail=False)
    def favorites(self, request, *args, **kwargs):
        """Возвращает список избранных карт."""

        favorite_cards = (
            self.request.user.cards.
            select_related('card', 'card__shop').
            prefetch_related('card__shop__group')
        ).filter(favourite=True)
        serializer = CardsListSerializer(
            favorite_cards,
            many=True,
        )
        return Response(serializer.data)

    @swagger_auto_schema(
        methods=['POST'],
        request_body=openapi.Schema(type=openapi.TYPE_OBJECT),
        responses={201: CardsListSerializer()},
        operation_summary='Добавление карты в избранное',
        operation_description='''
            Добавляет карту в избранное.
            '''
    )
    @swagger_auto_schema(
        methods=['DELETE'],
        responses={200: CardsListSerializer()},
        operation_summary='Удаление карты из избранного',
        operation_description='''
                Удаляет карту из избранного.
                '''
    )
    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        user = request.user
        user_card = get_object_or_404(UserCards, user=user, card__id=pk)
        if (
                (user_card.favourite and request.method == 'POST')
                or (not user_card.favourite and request.method == 'DELETE')
        ):
            raise serializers.ValidationError(
                'Статус карты уже соответствует запрашиваемому.')
        if request.method in ('POST', 'DELETE'):
            user_card.favourite = not user_card.favourite
            user_card.save()
            serializer = CardsListSerializer(
                user_card,
            )
            operation_status = (
                status.HTTP_201_CREATED if request.method == 'POST'
                else status.HTTP_200_OK
            )
            return Response(serializer.data, status=operation_status)

        raise serializers.ValidationError(
            {"errors": "Что-то пошло не так."}
        )

    @swagger_auto_schema(
        methods=['PATCH'],
        request_body=StatisticsSerializer(),
        responses={200: CardsListSerializer()},
        operation_summary='Увеличение счётчика использования',
        operation_description='''
            Присваивает счётчику использования карты число,
            переданное в теле запроса.
            Доступно только увеличение счётчика.
            '''
    )
    @action(detail=True, methods=['patch'], name='statistics')
    def statistics(self, request, pk):
        serializer = StatisticsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = request.user
            user_card = get_object_or_404(UserCards, user=user, card__id=pk)
            new_statistics = request.data['usage_counter']
            if user_card.usage_counter < int(new_statistics):
                user_card.usage_counter = new_statistics
                user_card.save()
                serializer = CardsListSerializer(user_card)
                return Response(serializer.data, status=status.HTTP_200_OK)
            raise StatisticsError


class ShopViewSet(viewsets.ModelViewSet):
    """Вьюсет для отображения единично и списком Магазинов."""

    http_method_names = ['patch', 'get', 'head']
    serializer_class = ShopSerializer
    permission_classes = (AllowAny,)
    queryset = Shop.objects.filter(validation=True)

    def get_queryset(self):
        if self.action == 'partial_update':
            return Shop.objects.all()
        return Shop.objects.filter(validation=True)

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return ShopCreateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'partial_update':
            return (IsShopCreatorOrReadOnly(),)
        return super().get_permissions()

    @swagger_auto_schema(
        responses={200: ShopSerializer()},
        operation_summary='Список верифицированных магазинов.',
        operation_description=(
            'Выдает список верифицированных категорий магазинов.'
        )
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={200: ShopSerializer()},
        operation_summary='Данные конкретного верифицированного магазина.',
        operation_description=(
            'Выдает данные конкретного верифицированного магазина.'
        )
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        request_body=ShopCreateSerializer(),
        responses={200: ShopSerializer()},
        operation_summary='Изменение магазина и его категории',
        operation_description='''
            Частично редактирует магазин,
            если он был создан текущим пользователем.
            '''
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для отображения единично и списком Категорий."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        responses={200: GroupSerializer()},
        operation_summary='Список категорий магазинов.',
        operation_description=(
            'Выдает список категорий магазинов.'
        )
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={200: GroupSerializer()},
        operation_summary='Данные конкретной категории магазина.',
        operation_description=(
            'Выдает данные конкретной категории магазина.'
        )
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
