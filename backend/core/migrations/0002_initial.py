# Generated by Django 3.2.22 on 2023-11-06 09:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='favourites',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_favourites', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='card',
            name='group',
            field=models.ManyToManyField(to='core.Group', verbose_name='Категории'),
        ),
        migrations.AddField(
            model_name='card',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
        ),
        migrations.AddField(
            model_name='card',
            name='shop',
            field=models.ForeignKey(blank=True, help_text='Выберите магазин', null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.shop', verbose_name='Магазин'),
        ),
        migrations.AddConstraint(
            model_name='favourites',
            constraint=models.UniqueConstraint(fields=('user', 'card'), name='uniq_favorites'),
        ),
    ]
