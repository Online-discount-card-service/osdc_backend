# Generated by Django 4.1 on 2023-12-01 11:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_card_usage_counter_usercards_usage_counter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='barcode_number',
            field=models.CharField(blank=True, max_length=40, validators=[django.core.validators.RegexValidator(message='Номер штрих-кода может содержать только буквы, цифры, пробелы,тире и нижнее подчеркивание.', regex='^[0-9A-Za-zА-Яа-я\\s-_]{1,40}$')], verbose_name='Номер штрих-кода'),
        ),
        migrations.AlterField(
            model_name='card',
            name='card_number',
            field=models.CharField(blank=True, max_length=40, validators=[django.core.validators.RegexValidator(message='Номер карты может содержать только буквы, цифры, пробелы, тиреи нижнее подчеркивание.', regex='^[0-9A-Za-zА-Яа-я\\s-_]{1,40}$')], verbose_name='Номер карты'),
        ),
        migrations.AlterField(
            model_name='card',
            name='name',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(message='Название может содержать только буквы, цифры, пробелыи спецсимволы.', regex='^[0-9a-zA-Zа-яА-ЯёЁ\\s\\S]{1,30}$')], verbose_name='Название карты'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='name',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(message='Название может содержать только буквы, цифры, пробелыи спецсимволы.', regex='^[0-9a-zA-Zа-яА-ЯёЁ\\s\\S]{1,30}$')], verbose_name='Название магазина'),
        ),
    ]
