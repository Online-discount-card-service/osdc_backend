from django.contrib.auth import get_user_model
from django.db import models

from .consts import (MAX_LENGTH_CARD_NAME, MAX_LENGTH_GROUP_NAME,
                     MAX_LENGTH_SHOP_NAME)

User = get_user_model()


class Group(models.Model):
    """Данный класс предназначен для создания в бд категорий"""
    name = models.CharField(
        max_length=MAX_LENGTH_GROUP_NAME,
        verbose_name='Название категории',
        help_text='Введите название категории'
    )
    # slug = models.SlugField(
    #     unique=True,
    #     max_length=50,
    #     verbose_name='Индентификатор категории',
    #     help_text='Введите индентификатор категории'
    # )

    class Meta:
        verbose_name = 'Категория',
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Shop(models.Model):
    """Клас предназначен для создания в бд перечня магазинов"""
    name = models.CharField(
        max_length=MAX_LENGTH_SHOP_NAME,
        verbose_name='Название магазина',
        help_text='Введите название магазина'
    )
    logo = models.ImageField(
        upload_to='shop/',
        verbose_name='Лого магазина',
        help_text='Загрузите логотип магазина'
    )
    group = models.ManyToManyField(
        Group,
        verbose_name='Категории'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.name


class Card(models.Model):
    """Класс предназначен для создания карты пользователя в бд"""
    name = models.CharField(
        max_length=MAX_LENGTH_CARD_NAME,
        blank=True,
        null=True,
        verbose_name='Название магазина',
        help_text='Введите название магазина',
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owner',
        verbose_name='Владелец'
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
        help_text='Загрузите изображение'
    )
    image_gtin = models.ImageField(
        upload_to='gtin/',
        verbose_name='Изображение штрих-кода',
        help_text='Загрузите изображение штрих-кода',
        blank=True
    )
    group = models.ManyToManyField(
        Group,
        verbose_name='Категории'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'

    def __str__(self):
        return self.name


class Favourites(models.Model):
    """Класс предназначет для хранения в бд списка избраных
    карт пользователя"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_favourites',
        verbose_name='Пользователь'
    )
    card = models.ForeignKey(
        Card,
        on_delete=models.CASCADE,
        related_name='card_favourites'
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
