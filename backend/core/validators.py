import re

from django.core.exceptions import ValidationError

from core.consts import ErrorMessage


def validate_color_format(value):
    if not re.match(r'^#[0-9a-fA-F]{3,6}$', value):
        raise ValidationError(ErrorMessage.INCORRECT_COLOR_FORMAT)
