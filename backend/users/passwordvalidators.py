import re

from django.core.exceptions import ValidationError

from core.consts import ErrorMessage


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
