# Generated by Django 4.1 on 2023-11-19 23:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='usercards',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='shop',
            name='group',
            field=models.ManyToManyField(blank=True, to='core.group', verbose_name='Категории'),
        ),
        migrations.AddField(
            model_name='card',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.shop', verbose_name='Магазин'),
        ),
        migrations.AddField(
            model_name='card',
            name='users',
            field=models.ManyToManyField(through='core.UserCards', to=settings.AUTH_USER_MODEL, verbose_name='Пользователи'),
        ),
        migrations.AddConstraint(
            model_name='usercards',
            constraint=models.UniqueConstraint(fields=('user', 'card'), name='uniq_favorites'),
        ),
    ]
