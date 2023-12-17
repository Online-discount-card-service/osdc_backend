# Generated by Django 4.1 on 2023-12-15 14:59

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages={'unique': 'Пользователь с таким email уже существует.'}, max_length=256, unique=True, validators=[users.models.no_cirrylic_email], verbose_name='Адрес электронной почты'),
        ),
    ]
