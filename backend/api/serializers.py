from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from core.consts import MAX_NUM_CARD_USE_BY_USER
from core.models import Card, Group, Shop, UserCards
from users.models import User


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор категорий."""

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
        )


class ShopSerializer(serializers.ModelSerializer):
    """Сериализатор магазина."""

    group = GroupSerializer(many=True)
    logo = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Shop
        fields = '__all__'

    def get_logo(self, obj):
        """Возвращает относительный путь изображения."""

        if obj.logo:
            return obj.logo.url
        return None


class CardSerializer(serializers.ModelSerializer):
    """Сериализатор отображения карт."""

    shop = ShopSerializer()
    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Card
        exclude = ('users',)

    def get_image(self, obj):
        """Возвращает относительный путь изображения."""

        if obj.image:
            return obj.image.url
        return None


class CardEditSerializer(serializers.ModelSerializer):
    """Сериализатор редактирования карты."""

    image = serializers.ImageField(required=False)
    shop = serializers.PrimaryKeyRelatedField(
        queryset=Shop.objects.all(),
        required=True,
    )

    class Meta:
        model = Card
        exclude = ('users',)

    def validate(self, data):
        """Проверка наличия номера карты и/или штрих-кода."""

        if not (
                data.get('card_number')
                or data.get('barcode_number')
        ):
            raise serializers.ValidationError(
                'Необходимо указать номер карты и/или штрих-кода')
        return data

    def to_representation(self, instance):
        return CardSerializer(instance).data


class CardsListSerializer(serializers.ModelSerializer):
    """Сериализатор списка карт пользователя."""

    card = CardSerializer()

    class Meta:
        model = UserCards
        exclude = ('id', 'user', )


class ShopCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания магазина с возможностью добавить категории."""

    name = serializers.CharField()
    group = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=False,
        queryset=Group.objects.all(),
        required=False
    )

    class Meta:
        model = Shop
        fields = ('name', 'group',)

    def to_representation(self, instance):
        return ShopSerializer(instance).data


class CardShopCreateSerializer(CardEditSerializer):
    """Сериализатор для создания карты с новым магазином."""

    shop = ShopCreateSerializer()

    def create(self, validated_data):
        shop_name = validated_data.pop('shop')
        shop = Shop.objects.create(name=shop_name['name'])
        if 'group' in shop_name:
            groups = shop_name['group']
            shop.group.set(groups)
        card = Card.objects.create(shop=shop, **validated_data)
        return card


class StatisticsSerializer(serializers.Serializer):
    """Сериализатор добавления статистики."""

    usage_counter = serializers.IntegerField(
        min_value=1,
        max_value=MAX_NUM_CARD_USE_BY_USER
    )


class UserCustomCreateSerializer(UserCreateSerializer):
    """Сериализатор регистрации пользователей."""

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'name',
            'phone_number',
            'password'
        )


class UserReadSerializer(UserSerializer):
    """Сериализатор отображения пользователей."""

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'name',
            'phone_number',
        )
