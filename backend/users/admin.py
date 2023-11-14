from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'username',
        'phone_number',
        'date_joined',
        'last_login',
    )
    list_filter = ('date_joined',)
    search_fields = ('email', 'username',)
    ordering = ('-date_joined',)
