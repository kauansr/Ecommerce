from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'data_joined','is_staff', 'is_active', 'is_superuser']
    fieldsets = (
        (None, {
            "fields": (
                ('email', 'username', 'password', 'data_joined', 'is_staff', 'is_active', 'is_superuser',)
                
            ),
        }),
    )

    add_fieldsets = ((None, {'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser'),}),)


    ordering = ['id']
    search_fields = ['email', 'username']


admin.site.register(User, CustomUserAdmin)