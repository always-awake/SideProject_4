from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    fieldsets = (('User Profile', {
        'fields': (
            'phone',
        )
    }),) + AuthUserAdmin.fieldsets

    list_display = (
        'username',
        'phone',
        'is_superuser',
    )
    
    search_fields = ['username']
