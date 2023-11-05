from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'username',
        'date_joined',
        'phone_number',
        'first_name'
    )
    list_filter = ('date_joined',)
    search_fields = ('email', 'username',)
    ordering = ('-date_joined',)
