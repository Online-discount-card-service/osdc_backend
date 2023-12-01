from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.consts import LEN_NUMBER, MAX_LENGTH_EMAIL, MAX_LENGTH_NAME


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        """Создает и сохраняет пользователя с указанным email и паролем."""

        if not email:
            raise ValueError(_('Электронная почта должна быть установлена'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Класс переопределяет стандартную модель User."""

    email = models.EmailField(
        verbose_name=_("Адрес электронной почты"),
        unique=True,
        blank=False,
        error_messages={
            'unique': _('Пользователь с таким email уже существует')
        },
        max_length=MAX_LENGTH_EMAIL
    )
    name = models.CharField(
        verbose_name=_("Имя"),
        unique=False,
        blank=False,
        max_length=MAX_LENGTH_NAME,
        validators=[RegexValidator(
            regex=r'^[a-zA-Zа-яА-ЯёЁ\s\S]{1,60}$',
            message='Имя может содержать только буквы, пробелы и спецсимволы.',
        )]
    )

    username = None

    phone_number = models.CharField(
        verbose_name=_("Телефон"),
        max_length=LEN_NUMBER,
        validators=[RegexValidator(
            regex=r'^\d{10}$',
            message='Номер телефона после +7 начинается с 9'
        )],
        blank=False,
    )

    is_active = models.BooleanField(
        verbose_name=('Почта подтверждена'),
        default=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone_number']

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return f'{self.name}({self.email})'
