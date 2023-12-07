# Generated by Django 4.1 on 2023-12-07 16:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages={'unique': 'Пользователь с таким email уже существует.'}, max_length=30, unique=True, verbose_name='Адрес электронной почты'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Номер телефона 10 цифр после +7.', regex='^\\d{10}$')], verbose_name='Телефон'),
        ),
    ]
