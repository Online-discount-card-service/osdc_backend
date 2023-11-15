from core.models import Card, Group, Shop, UserCards
from django.contrib import admin


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
        'color',
        'validation',
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
        'shop',
        'pub_date',
        'card_number',
        'barcode_number',
        'encoding_type',
        'usage_counter'
    )
    empty_value_display = '-пусто-'
    search_fields = (
        'name',
        'shop',
        'pub_date',
        'card_number',
        'barcode_number',
        'encoding_type',
    )
    list_filter = (
        'name',
        'shop',
        'pub_date',
        'card_number',
        'barcode_number',
        'encoding_type',
    )


@admin.register(UserCards)
class UserCardsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'card',
        'owner',
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
