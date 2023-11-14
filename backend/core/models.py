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
    """Данный класс предназначен для создания в бд категорий."""

    name = models.CharField(
        max_length=MAX_LENGTH_GROUP_NAME,
        verbose_name='Название категории',
        help_text='Введите название категории'
    )

    class Meta:
        verbose_name = 'Категория',
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Shop(models.Model):
    """Клас предназначен для создания в бд перечня магазинов."""

    name = models.CharField(
        max_length=MAX_LENGTH_SHOP_NAME,
        verbose_name='Название карты',
        help_text='Назовите карту'
    )
    group = models.ManyToManyField(
        Group,
        verbose_name='Категории'
    )
    logo = models.ImageField(
        upload_to='shop/',
        verbose_name='Лого магазина',
        help_text='Загрузите логотип магазина'
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
    """Класс предназначен для создания карты пользователя в бд."""

    name = models.CharField(
        max_length=MAX_LENGTH_CARD_NAME,
        blank=False,
        verbose_name='Название карты',
        help_text='Введите название карты',
        unique=True
    )
    shop = models.ForeignKey(
        Shop,
        on_delete=models.SET_NULL,
        verbose_name='Магазин',
        help_text='Выберите магазин',
        blank=True,
        null=True
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления карты',
        auto_now_add=True,
    )
    image_card = models.ImageField(
        upload_to='card/',
        verbose_name='Изображение карты',
        help_text='Загрузите изображение',
        blank=True,
    )
    card_number = models.CharField(
        max_length=MAX_LENGTH_CARD_NUMBER,
        verbose_name='Номер карты',
        help_text='Введите номер карты',
        blank=True
    )
    barcode_number = models.CharField(
        max_length=MAX_LENGTH_CARD_NUMBER,
        verbose_name='Номер штрих-кода',
        help_text='Введите номер штрих-кода',
        blank=True
    )
    encoding_type = models.CharField(
        max_length=MAX_LENGTH_ENCODING_TYPE,
        verbose_name='Тип кодировки бар-кода карты',
        choices=ENCODING_TYPE,
        default=EAN_13
    )
    usage_counter = models.PositiveBigIntegerField(
        verbose_name='Количество использования карты',
        default=0,
        blank=True
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
        related_name='user_favourites',
        verbose_name='Пользователь'
    )
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name='card_favourites',
        verbose_name='Карты'
    )
    owner = models.BooleanField(
        verbose_name='Принадлежность',
        blank=True,
        default=True,
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
        verbose_name = 'Список избранного'
        verbose_name_plural = 'Список избранного'
        ordering = ('user',)

    def __str__(self):
        return f'{self.card} в списке избранного пользователя {self.user}'
