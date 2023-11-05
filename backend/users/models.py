from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from users.consts import (MAX_LENGTH_NAME,
                          LEN_NUMBER,
                          MAX_LENGTH_EMAIL,
                          MAX_LENGTH_USERNAME,
                          MAX_LENGTH_PASSWORD)


class User(AbstractUser):
    """Класс переопределяет стандартную модель User"""
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
        verbose_name=_("Ваше имя"),
        unique=True,
        blank=True,
        max_length=MAX_LENGTH_USERNAME,
        help_text=_('Укажите свое имя'),
    )
    first_name = models.CharField(
        verbose_name=_('first name'),
        max_length=MAX_LENGTH_NAME,
        blank=True
    )
    phone_number = PhoneNumberField(
        region="RU",
        max_length=LEN_NUMBER,
        blank=False
    )
    password = models.CharField(
        verbose_name=_('Пароль'),
        help_text=_('Введите пароль'),
        max_length=MAX_LENGTH_PASSWORD,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.email
