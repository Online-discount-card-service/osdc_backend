# Generated by Django 4.1 on 2023-12-13 14:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_usercards_options_usercards_pub_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='barcode_number',
            field=models.CharField(blank=True, max_length=256, validators=[django.core.validators.RegexValidator(message='Номер штрих-кода может содержать только буквы, цифры, пробелы, тире и нижнее подчеркивание.', regex='^[0-9A-Za-zА-Яа-я\\ \\-_]{1,40}$')], verbose_name='Номер штрих-кода'),
        ),
        migrations.AlterField(
            model_name='group',
            name='name',
            field=models.CharField(max_length=30, verbose_name='Название категории'),
        ),
    ]
