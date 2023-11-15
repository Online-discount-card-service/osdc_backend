from django.core.exceptions import ValidationError
from users.consts import RESERVED_USERNAMES


def validate_username_in_reserved_list(value):
    if value.lower() in RESERVED_USERNAMES:
        raise ValidationError('Имя пользователя зарезервировано.')
