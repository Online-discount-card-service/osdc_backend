# Generated by Django 4.1 on 2023-11-15 21:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default='Безымянный', help_text='Укажите свое имя', max_length=60, validators=[django.core.validators.RegexValidator(message='Имя может содержать только буквы, пробелы и тире', regex='^[a-zA-Zа-яА-Я\\s-]{1,60}$')], verbose_name='Имя'),
            preserve_default=False,
        ),
    ]
