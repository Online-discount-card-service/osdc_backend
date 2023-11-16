import base64

from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from core.models import Card, Group, Shop
from users.models import User


class Base64ImageField(serializers.ImageField):
    """Кастомное поле для изображений."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class GroupSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Категории."""

    class Meta:
        model = Group
        fields = (
            'id',
            'name'
        )


class ShopSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Магазины."""

    group = GroupSerializer(many=True)

    class Meta:
        model = Shop
        fields = '__all__'


# class ShopCreateSerializer(serializers.ModelSerializer):
    # """Сериализатор для создания Магазина."""

    # class Meta:
        # model = Shop
        # fields = 'name'


class CardSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Карты."""

    owner = UserSerializer(read_only=True)
    shop = serializers.PrimaryKeyRelatedField(
        queryset=Shop.objects.all(), required=False)
    image_card = Base64ImageField(required=False)

    class Meta:
        model = Card
        fields = (
            'id',
            'name',
            'owner',
            'shop',
            'image_card',
            'card_number',
            'barcode_number',
        )

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.image_card = validated_data.get(
            'image_card',
            instance.image_card
        )
        instance.card_number = validated_data.get(
            'card_number',
            instance.card_number
        )
        instance.barcode_number = validated_data.get(
            'barcode_number',
            instance.barcode_number
        )
        instance.shop = validated_data.get('shop', instance.shop)
        instance.save()
        return instance

    def to_representation(self, instance):
        return CardReadSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data


class CardReadSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения модели Карты."""

    shop = ShopSerializer()

    class Meta:
        model = Card
        fields = (
            'id',
            'name',
            'shop',
            'image_card',
            'card_number',
            'barcode_number',
            'group'
        )


class CardForUserSerializer(serializers.ModelSerializer):
    """Сериализатор для Карт при запросе на эндпоинт api/users."""

    shop = serializers.PrimaryKeyRelatedField(
        queryset=Shop.objects.all())

    class Meta:
        model = Card
        fields = (
            'id',
            'name',
            'shop',
            'image_card',
            'card_number',
            'barcode_number',
            'group'
        )


class UserCustomCreateSerializer(UserCreateSerializer):
    """Сериализатор для регистрации новых Пользователей."""

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'phone_number',
            'password'
        )


class UserReadSerializer(UserSerializer):
    """Сериализатор для чтения модели Пользователь."""

    # cards = CardForUserSerializer(many=True)

    class Meta:
        model = User
        # Выключено пока нет подтверждения что отдаем все при запросе с
        # пользователем
        # is_favorite = serializers.BooleanField()
        # card = serializers.CardSerializer(many=True)
        fields = (
            'id',
            'email',
            'username',
            'phone_number',
        )
