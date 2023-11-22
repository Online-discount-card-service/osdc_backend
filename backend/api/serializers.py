from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

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

    class Meta:
        model = Shop
        fields = '__all__'


class CardSerializer(serializers.ModelSerializer):
    """Сериализатор отображения карт."""

    shop = ShopSerializer()

    class Meta:
        model = Card
        exclude = ('users', )


class CardEditSerializer(serializers.ModelSerializer):
    """Сериализатор редактирования карты."""

    image = serializers.ImageField(required=False)
    shop = serializers.PrimaryKeyRelatedField(
        queryset=Shop.objects.all(),
        required=True,
    )

    class Meta:
        model = Card
        exclude = ('users', 'usage_counter')

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


class ShopCreateSerializer(serializers.Serializer):
    """Сериализатор создания магазина."""

    name = serializers.CharField()

    class Meta:
        model = Shop
        fields = ('name',)


class CardShopCreateSerializer(CardEditSerializer):
    """Сериализатор для создания карты с новым магазином."""

    shop = ShopCreateSerializer()

    def create(self, validated_data):
        shopname = validated_data.pop('shop')
        shop = Shop.objects.create(name=shopname['name'])
        card = Card.objects.create(shop=shop, **validated_data)
        return card


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
