from djoser.serializers import UserCreateSerializer, UserSerializer
from users.models import User


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
