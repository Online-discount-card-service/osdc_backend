import re

from django.core.exceptions import ValidationError

from core.consts import ErrorMessage


def no_cirrylic_email(email):
    if re.findall(r'[ЁёА-я]', email):
        raise ValidationError(f'{ErrorMessage.INCORRECT_EMAIL}')
    return email
