from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from users.consts import MAX_LENGTH_NAME, LEN_NUMBER


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
    )
    # При необходимости раздельного хранения имени и Фамили
    # first_name = models.CharField(max_length=MAX_LENGTH_NAME, blank=True, verbose_name="Имя")
    # last_name = models.CharField(max_length=MAX_LENGTH_NAME, blank=True, verbose_name="Фамилия")
    username = models.CharField(
        verbose_name=_("Ваше имя"),
        unique=True,
        blank=True,
        max_length=MAX_LENGTH_NAME,
        help_text=_('Укажите свое имя'),
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Дата регистрации")
    )
    phone_number = PhoneNumberField(
        region="RU",
        max_length=LEN_NUMBER,
        blank=False
    )
    password = models.CharField(
        verbose_name=_('Пароль'),
        help_text=_('Введите пароль'),
        max_length=150,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.email
