from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from users.models import User
from core.models import Card, Shop, Group


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


class UserCreateSerializer(UserCreateSerializer):
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


class ShopSerializer(serializers.ModelSerializer):
    """ """
    class Meta:
        model = Shop
        fields = '__all__'


class CardSerializer(serializers.ModelSerializer):
    """ """
    class Meta:
        model = Card
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    """ """
    class Meta:
        model = Group
        fields = '__all__'
