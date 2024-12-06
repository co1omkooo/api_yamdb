from django.contrib import admin

from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'first_name',
        'email',
        'bio',
        'role'
    )


admin.site.register(User, UserAdmin)
