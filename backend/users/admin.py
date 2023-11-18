from django.contrib import admin

from users.models import User


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
