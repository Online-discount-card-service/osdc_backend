# Generated by Django 4.1 on 2023-11-16 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_merge_20231116_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='group',
            field=models.ManyToManyField(blank=True, to='core.group', verbose_name='Категории'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='logo',
            field=models.ImageField(blank=True, help_text='Загрузите логотип магазина', null=True, upload_to='shop/', verbose_name='Лого магазина'),
        ),
    ]
