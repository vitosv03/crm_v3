from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext, gettext_lazy as _
from .models import Users
# from .models import Users


# Register your models here.

class UsersAdmin(BaseUserAdmin):
    """
    add Users to admin and config it
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'image', 'date_created',
                    'date_updated', 'get_image',)
    readonly_fields = ('date_created', 'date_updated', 'get_image',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('dates'), {'fields': ('date_created', 'date_updated')}),
        (_('Profile Photo'), {'fields': ('image', 'get_image')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'image', ),
        }),
    )

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} width="100" height="100">')

    get_image.short_description = 'image'


admin.site.register(Users, UsersAdmin)



