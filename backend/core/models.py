from django.contrib.auth import get_user_model
from django.db import models

from .consts import (
    EAN_13,
    ENCODING_TYPE,
    MAX_LENGTH_CARD_NAME,
    MAX_LENGTH_CARD_NUMBER,
    MAX_LENGTH_COLOR,
    MAX_LENGTH_ENCODING_TYPE,
    MAX_LENGTH_GROUP_NAME,
    MAX_LENGTH_SHOP_NAME,
)
from .validators import validate_color_format


User = get_user_model()


class Group(models.Model):
    """Класс для представления Категории."""

    name = models.CharField(
        max_length=MAX_LENGTH_GROUP_NAME,
        verbose_name='Название категории',
    )

    class Meta:
        verbose_name = 'Категория',
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Shop(models.Model):
    """Клас для представления магазинов."""

    name = models.CharField(
        max_length=MAX_LENGTH_SHOP_NAME,
        verbose_name='Название магазина',
    )
    group = models.ManyToManyField(
        Group,
        verbose_name='Категории',
        blank=True
    )
    logo = models.ImageField(
        upload_to='shop/',
        verbose_name='Лого магазина',
        null=True,
        blank=True
    )
    color = models.CharField(
        verbose_name='Цвет магазина',
        max_length=MAX_LENGTH_COLOR,
        validators=[validate_color_format],
        blank=True,
    )
    validation = models.BooleanField(
        verbose_name='Критерий валидации магазина',
        blank=True,
        default=False,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.name


class Card(models.Model):
    """Класс для представления Карт."""

    name = models.CharField(
        max_length=MAX_LENGTH_CARD_NAME,
        blank=False,
        verbose_name='Название карты',
    )
    shop = models.ForeignKey(
        Shop,
        on_delete=models.PROTECT,
        verbose_name='Магазин',
        blank=False,
        null=False,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления карты',
        auto_now_add=True,
    )
    image = models.ImageField(
        upload_to='card/',
        verbose_name='Изображение карты',
        blank=True,
    )
    card_number = models.CharField(
        max_length=MAX_LENGTH_CARD_NUMBER,
        verbose_name='Номер карты',
        blank=True
    )
    barcode_number = models.CharField(
        max_length=MAX_LENGTH_CARD_NUMBER,
        verbose_name='Номер штрих-кода',
        blank=True
    )
    encoding_type = models.CharField(
        max_length=MAX_LENGTH_ENCODING_TYPE,
        verbose_name='Тип кодировки бар-кода карты',
        choices=ENCODING_TYPE,
        default=EAN_13,
        blank=True
    )
    usage_counter = models.PositiveBigIntegerField(
        verbose_name='Количество использований карты',
        default=0,
        blank=True
    )
    users = models.ManyToManyField(
        User,
        through='UserCards',
        through_fields=('card', 'user'),
        verbose_name='Пользователи',
        blank=False
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'

    def __str__(self):
        return self.name


class UserCards(models.Model):
    """Карты пользователя."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cards',
        verbose_name='Пользователь'
    )
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name='Карты'
    )
    owner = models.BooleanField(
        verbose_name='Принадлежность',
        blank=True,
        default=True,
    )
    favourite = models.BooleanField(
        verbose_name='Избранное',
        blank=True,
        default=False,
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=[
                    'user',
                    'card'
                ],
                name='uniq_favorites'
            ),
        )
        verbose_name = 'Карта пользователя'
        verbose_name_plural = 'Список карт пользователя'
        ordering = ('user',)

    def __str__(self):
        return f'{self.card} в списке карт пользователя {self.user}'
