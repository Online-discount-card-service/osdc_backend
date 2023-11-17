from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from core.models import Card, Group, Shop

from users.models import User


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Категории."""

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
        )


class ShopSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Магазины."""

    group = GroupSerializer(many=True)

    class Meta:
        model = Shop
        fields = '__all__'


class CardSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Карты."""

    # shop = serializers.PrimaryKeyRelatedField(
    #     queryset=Shop.objects.all(),
    #     required=False,
    # )

    shop = ShopSerializer()

    image = serializers.SerializerMethodField(
        'get_image_url',
        read_only=True,
    )

    class Meta:
        model = Card
        fields = (
            'id',
            'name',
            'shop',
            'image_card',
            'card_number',
            'barcode_number',
            'encoding_type',
            'usage_counter',
        )

    def get_image_url(self, obj):
        """Возвращает относительный путь изображения."""
        if obj.image:
            return obj.image.url
        return None

    def update(self, instance, validated_data):
        instance.name = validated_data.get(
            'name',
            instance.name
        )
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
        instance.shop = validated_data.get(
            'shop',
            instance.shop
        )
        instance.name = validated_data.get(
            'encoding_type',
            instance.encoding_type
        )
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
            'encoding_type',
            'usage_counter',
        )


class CardForUserSerializer(serializers.ModelSerializer):
    """Сериализатор для Карт при запросе на эндпоинт api/users."""

    shop = serializers.PrimaryKeyRelatedField(queryset=Shop.objects.all())

    class Meta:
        model = Card
        fields = (
            'id',
            'name',
            'shop',
            'image_card',
            'card_number',
            'barcode_number',
            'encoding_type',
            'usage_counter',
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
