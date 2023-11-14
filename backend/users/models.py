from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
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
        unique=True,
        verbose_name=_("Адрес электронной почты"),
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

    phone_number = PhoneNumberField(
        region="RU",
        max_length=LEN_NUMBER,
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
