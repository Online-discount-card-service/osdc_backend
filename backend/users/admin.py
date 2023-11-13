from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'username',
        'phone_number',
        'pub_date',
    )
    list_filter = ('pub_date',)
    search_fields = ('email', 'username',)
    ordering = ('-pub_date',)
