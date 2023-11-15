from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.consts import (
    LEN_NUMBER,
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_PASSWORD,
    MAX_LENGTH_USERNAME,
)
from users.validators import validate_username_in_reserved_list


class User(AbstractUser):
    """Класс переопределяет стандартную модель User."""

    email = models.EmailField(
        verbose_name=_("Адрес электронной почты"),
        unique=True,
        blank=False,
        error_messages={
            'unique': _('Пользователь с таким email уже существует')
        },
        help_text=_('Укажите свой email'),
        max_length=MAX_LENGTH_EMAIL
    )
    username = models.CharField(
        verbose_name=_("Username"),
        unique=False,
        blank=False,
        max_length=MAX_LENGTH_USERNAME,
        help_text=_('Укажите username'),
        validators=[
            validate_username_in_reserved_list,
            UnicodeUsernameValidator(),
        ]
    )
    phone_number = models.CharField(
        max_length=LEN_NUMBER,
        validators=[RegexValidator(
            regex=r'^([9]{1}[0-9]{9})?$',
            message='Номер телефона после +7 начинается с 9'
        )],
        blank=False,
        unique=True
    )
    password = models.CharField(
        verbose_name=_('Пароль'),
        help_text=_('Введите пароль'),
        max_length=MAX_LENGTH_PASSWORD,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.email
