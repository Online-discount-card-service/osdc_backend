from django.contrib import admin

from core.models import Card, Favourites, Group, Shop


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name'
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'name',
    )


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'logo',
    )
    empty_value_display = '-пусто-'
    search_fields = (
        'name',
        'logo',
    )
    list_filter = (
        'name',
    )


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'owner',
        'pub_date',
        'shop',
        'card_number',
        'barcode_number'
    )
    empty_value_display = '-пусто-'
    search_fields = (
        'name',
        'owner',
        'pub_date',
        'shop',
        'card_number',
        'barcode_number'
    )
    list_filter = (
        'name',
        'owner',
        'pub_date',
        'shop',
        'card_number',
        'barcode_number'
    )


@admin.register(Favourites)
class FavouritesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'card',
    )
    empty_value_display = '-пусто-'
    search_fields = (
        'user',
        'card',
    )
    list_filter = (
        'user',
        'card',
    )
