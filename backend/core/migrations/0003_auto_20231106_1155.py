# Generated by Django 3.2.22 on 2023-11-06 06:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='name',
            field=models.CharField(blank=True, help_text='Введите название магазина', max_length=20, null=True, verbose_name='Название магазина'),
        ),
        migrations.RemoveField(
            model_name='card',
            name='shop',
        ),
        migrations.AddField(
            model_name='card',
            name='shop',
            field=models.ForeignKey(blank=True, help_text='Выберите магазин', null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.shop', verbose_name='Магазин'),
        ),
    ]
