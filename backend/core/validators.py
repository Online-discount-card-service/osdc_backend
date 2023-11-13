import re

from django.core.exceptions import ValidationError


def validate_color_format(value):
    if not re.match(r'^#[0-9a-fA-F]{3,6}$', value):
        raise ValidationError(
            'Неверный формат для цвета, должно быть #AABBCC или #ABC'
        )
