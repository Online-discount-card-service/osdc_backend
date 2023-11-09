# Generated by Django 3.2.22 on 2023-11-06 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20231106_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='barcode_number',
            field=models.CharField(blank=True, help_text='Введите номер штрих-кода', max_length=150, verbose_name='Номер штрих-кода'),
        ),
        migrations.AlterField(
            model_name='card',
            name='card_number',
            field=models.CharField(blank=True, help_text='Введите номер карты', max_length=150, verbose_name='Номер карты'),
        ),
        migrations.AlterField(
            model_name='card',
            name='image_card',
            field=models.ImageField(blank=True, help_text='Загрузите изображение', upload_to='card/', verbose_name='Изображение карты'),
        ),
        migrations.AlterField(
            model_name='card',
            name='name',
            field=models.CharField(default=1, help_text='Введите название магазина', max_length=20, verbose_name='Название магазина'),
            preserve_default=False,
        ),
    ]