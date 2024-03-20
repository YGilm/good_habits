from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'is_staff', 'is_active', ]
    list_filter = ['email', 'is_staff', 'is_active', 'city', ]
    ordering = ('email',)
    search_fields = ('email', 'phone', 'city',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('phone', 'city', 'avatar', 'chat_id')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups')}),
    )
