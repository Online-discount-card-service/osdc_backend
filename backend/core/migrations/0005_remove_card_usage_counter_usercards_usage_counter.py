# Generated by Django 4.1 on 2023-11-25 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_usercards_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='usage_counter',
        ),
        migrations.AddField(
            model_name='usercards',
            name='usage_counter',
            field=models.PositiveBigIntegerField(blank=True, default=0, verbose_name='Количество использований карты'),
        ),
    ]
