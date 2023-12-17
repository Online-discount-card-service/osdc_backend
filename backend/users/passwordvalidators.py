import re

from django.core.exceptions import ValidationError

from core.consts import ErrorMessage
from users.consts import MAX_LENGTH_PASSWORD


class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall(r'\d', password):
            raise ValidationError(ErrorMessage.PASSWORD_NO_NUMBERS)


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-ZА-ЯЁ]', password):
            raise ValidationError(ErrorMessage.PASSWORD_NO_UPPER_CASE)


class LowercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[a-zа-яё]', password):
            raise ValidationError(ErrorMessage.PASSWORD_NO_LOWER_CASE)


class OnlyASCIIValidator(object):
    def validate(self, password, user=None):
        if not password.isascii():
            raise ValidationError(f'{ErrorMessage.INCORRECT_PASSWORD}')


class MaximumLengthValidator(object):
    def validate(self, password, user=None):
        if len(password) > MAX_LENGTH_PASSWORD:
            raise ValidationError(f'{ErrorMessage.PASSWORD_TOO_LONG}')
