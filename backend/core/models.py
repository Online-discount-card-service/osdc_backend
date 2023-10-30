from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Shop(models.Model):
    """Клас предназначен для создания в бд перечня магазинов"""
    name = models.CharField(
        max_length=200,
        verbose_name='Название магазина',
        help_text='Введите название магазина'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Индентификатор магазина',
        help_text='Введите индентификатор магазина'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'

    def __str__(self):
        return self.name


class Card(models.Model):
    """Класс предназначен для создания карты пользователя в бд"""
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owner',
        verbose_name='Владелец'
    )
    shop = models.ManyToManyField(
        Shop,
        verbose_name='Магазин',
        help_text='Выберите магазин'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добовления карты',
        auto_now_add=True,
    )
    image = models.ImageField(
        upload_to='card/',
        verbose_name='Изображение карты',
        help_text='Загрузите изображение'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Карта'
        verbose_name_plural = 'Карты'

    def __str__(self):
        return self.name
