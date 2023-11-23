from django.contrib import admin

from core.models import UserCards
from users.models import User


class CardsInline(admin.TabularInline):
    model = UserCards
    extra = 1


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'name',
        'phone_number',
        'date_joined',
        'last_login',
    )
    list_filter = ('date_joined',)
    search_fields = ('email', 'phone_number',)
    ordering = ('-date_joined',)

    inlines = [CardsInline]

    fieldsets = (
        (None, {
            'fields': (
                ('name', 'email', 'phone_number',),
                ('date_joined', 'last_login',),
                ('is_active', 'is_staff', 'is_superuser',)
            )
        }),
    )

    readonly_fields = ('last_login', 'date_joined',)
