from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'role',
        'is_staff',
        'confirmation_code',
        'is_superuser',
    )
    list_editable = (
        'role',
        'is_staff',
        'confirmation_code',
    )
    empty_value_display = '-пусто-'


admin.site.register(CustomUser, CustomUserAdmin)
