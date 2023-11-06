import base64

from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from django.core.files.base import ContentFile

from core.models import Card, Group, Shop
from users.models import User


class Base64ImageField(serializers.ImageField):
    """
    Кастмное поле для изображений.
    """
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class UserSerializer(UserSerializer):
    """Класс реализует серилизацию и десерилизацию данных
    о пользователях"""

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'phone_number',
        )


class UserCustomCreateSerializer(UserCreateSerializer):
    """ Класс реализует серилизацию и десерилизацию данных
    для регистрации новых пользователей"""
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'phone_number',
            'password'
        )


class UserCreatePasswordRetypeSerializer(UserCustomCreateSerializer):
    default_error_messages = {
        "password_mismatch": 'settings.CONSTANTS.messages.PASSWORD_MISMATCH_ERROR'  # Прописать свое
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["re_password"] = serializers.CharField(
            style={"input_type": "password"}
        )

    def validate(self, attrs):
        self.fields.pop("re_password", None)
        re_password = attrs.pop("re_password")
        attrs = super().validate(attrs)
        if attrs["password"] == re_password:
            return attrs
        else:
            self.fail("password_mismatch")


class GroupSerializer(serializers.ModelSerializer):
    """ """

    class Meta:
        model = Group
        fields = (
            'id',
            'name'
        )


class ShopSerializer(serializers.ModelSerializer):
    """ """
    group = GroupSerializer(many=True)

    class Meta:
        model = Shop
        fields = '__all__'


class CardSerializer(serializers.ModelSerializer):
    """ """
    owner = UserSerializer(read_only=True)
    shop = serializers.StringRelatedField()
    image_card = Base64ImageField()

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
            'group'
        )
