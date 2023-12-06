import re

from django.core.exceptions import ValidationError


class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall(r'\d', password):
            raise ValidationError(
                'Пароль должен содержать как минимум одну цифру, 0-9.'
            )


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-ZА-ЯЁ]', password):
            raise ValidationError(
                'Пароль должен содержать как минимум одну большую букву, '
                'A-Z или А-Я.'
            )


class LowercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[a-zа-яё]', password):
            raise ValidationError(
                'Пароль должен содержать как минимум одну маленькую букву, '
                'a-z или а-я.'
            )
