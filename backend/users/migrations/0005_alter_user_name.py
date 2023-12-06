# Generated by Django 4.1 on 2023-12-06 19:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_name_alter_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=60, validators=[django.core.validators.RegexValidator('^[a-zA-Zа-яА-ЯёЁ\\ \\!@#$%^&*()_+{}\\[\\]:;<>,.?~\\\\/\\-=|\\"\']+$', message='Имя может содержать только буквы, пробелы и спецсимволы.')], verbose_name='Имя'),
        ),
    ]