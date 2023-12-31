from django.contrib import admin

from core.models import Card, Group, Shop, UserCards


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    list_filter = ('name',)


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


class UsersInline(admin.TabularInline):
    model = UserCards
    extra = 1


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
    fieldsets = (
        (None, {
            'fields': (
                ('name', 'shop',),
                ('card_number', 'barcode_number', 'encoding_type',),
                ('pub_date',),
                ('image',),
            )
        }),
    )
    readonly_fields = ('pub_date',)
    inlines = [UsersInline]


@admin.register(UserCards)
class UserCardsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'card',
        'owner',
        'pub_date',
        'shared_by',
        'usage_counter'
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
