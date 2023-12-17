# Generated by Django 4.1 on 2023-12-16 08:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_alter_card_barcode_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='name',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Zа-яА-ЯёЁ\\ \\!@#$%^&*`_+{}\\[\\].?~\\\\\\/\\-=|\\"\']{1,30}$', message='Имя может содержать только буквы, пробелы и спецсимволы.')], verbose_name='Название карты'),
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Zа-яА-ЯёЁ\\ \\!@#$%^&*`_+{}\\[\\].?~\\\\\\/\\-=|\\"\']{1,30}$', message='Имя может содержать только буквы, пробелы и спецсимволы.')], verbose_name='Название категории'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='name',
            field=models.CharField(max_length=30, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Zа-яА-ЯёЁ\\ \\!@#$%^&*`_+{}\\[\\].?~\\\\\\/\\-=|\\"\']{1,30}$', message='Имя может содержать только буквы, пробелы и спецсимволы.')], verbose_name='Название магазина'),
        ),
    ]