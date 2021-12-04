from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from .models import Users


# Register your models here.

class UsersAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'image')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Profile Photo'), {'fields': ('image', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'image'),
        }),
    )


admin.site.register(Users, UsersAdmin)

