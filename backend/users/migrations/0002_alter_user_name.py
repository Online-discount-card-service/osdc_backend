# Generated by Django 4.1 on 2023-11-27 07:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=60, validators=[django.core.validators.RegexValidator(message='Имя может содержать только буквы, пробелы и тире', regex='^[a-zA-Zа-яА-ЯёЁ\\s-]{1,60}$')], verbose_name='Имя'),
        ),
    ]
