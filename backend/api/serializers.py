from difflib import SequenceMatcher

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import (
    CommonPasswordValidator,
    NumericPasswordValidator,
)
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from djoser.conf import settings
from djoser.serializers import (
    SendEmailResetSerializer,
    TokenCreateSerializer,
    UserCreateSerializer,
    UserSerializer,
)
from rest_framework import serializers

from core.consts import MAX_NUM_CARD_USE_BY_USER
from core.models import Card, Group, Shop, UserCards
from users.consts import MAX_SIMILARITY, MIN_PASSWORD_LENGTH
from users.models import User
from users.passwordvalidators import (
    LowercaseValidator,
    NumberValidator,
    UppercaseValidator,
)


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


class CustomUserCreateSerializer(UserCreateSerializer):
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


class UserPreCheckSerializer(serializers.ModelSerializer):
    """Сериализатор для проверки почты и пароля."""

    password = serializers.CharField(
        min_length=MIN_PASSWORD_LENGTH,
        required=True,
    )

    class Meta:
        model = User
        fields = ('email', 'password')

    def validate(self, data):
        password = data.get('password')
        email = data.get('email')
        sequence_matcher = SequenceMatcher(a=password.lower(), b=email.lower())
        if sequence_matcher.quick_ratio() > MAX_SIMILARITY:
            raise serializers.ValidationError("Пароль слишком похож на е-мейл")
        return super(UserPreCheckSerializer, self).validate(data)

    def validate_password(self, data):
        errors = []
        password_validators = (
            NumericPasswordValidator,
            NumberValidator,
            UppercaseValidator,
            LowercaseValidator
        )
        try:
            validator = CommonPasswordValidator()
            validator.validate(password=data, user=None)
        except ValidationError as error:
            errors.append(error)
        for validator in password_validators:
            try:
                validator.validate(self, password=data, user=None)
            except ValidationError as error:
                errors.append(error)
        if errors:
            raise ValidationError(errors)
        return data


class CustomTokenCreateSerializer(TokenCreateSerializer):
    """Выдает токен. Не проверяет активирован ли пользователь."""

    def validate(self, attrs):
        password = attrs.get('password')
        params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}
        self.user = authenticate(
            request=self.context.get("request"), **params, password=password
        )
        if not self.user:
            self.user = User.objects.filter(**params).first()
            if self.user and not self.user.check_password(password):
                self.fail("invalid_credentials")
        if self.user:
            return attrs
        self.fail("invalid_credentials")


class CustomSendEmailResetSerializer(SendEmailResetSerializer):
    phone_last_digits = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r'^\d{4}$',
                message='Здесь должны быть последние 4 цифры телефона.',
            )
        ]
    )

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if not User.objects.filter(
                phone_number__endswith=attrs['phone_last_digits'],
                email=attrs['email']
        ).exists():
            raise serializers.ValidationError('Неверные данные пользователя.')
        return attrs
