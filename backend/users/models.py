from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

# from core.models import CardQuerySet
from users.consts import (
    LEN_NUMBER,
    MAX_LENGTH_EMAIL,
    # MAX_LENGTH_NAME,
    MAX_LENGTH_PASSWORD,
    MAX_LENGTH_USERNAME,
)




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
        verbose_name=_("Ваше имя"),
        unique=False,
        blank=False,
        max_length=MAX_LENGTH_USERNAME,
        help_text=_('Укажите свое имя'),
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
    # objects отключено пока не решено, при подключении необходимо проверить
    # objects = CardQuerySet.as_manager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.email
