from django.contrib import admin
from django.utils.translation import gettext, gettext_lazy as _

from .models import ClientsInfo, ClientsEmails, ClientsPhones


# Register your models here.

@admin.register(ClientsInfo)
class ClientsInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'head', 'summary', 'display_phoneNumber', 'display_email', 'created_by', 'date_created',
                    'date_updated',)

    fieldsets = (
        (None, {'fields': ('title', 'head', 'summary')}),
        (_('Contacts'), {'fields': ('phoneNumber', 'email',)}),
        (_('Created_by'), {'fields': ('created_by',)}),
        (_('Dates'), {'fields': ('date_created', 'date_updated')}),
    )

    readonly_fields = ('date_created', 'date_updated', 'created_by')

    add_fieldsets = (
        (None, {
            'fields': ('title', 'head', 'phoneNumber', 'email'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        # obj.modified_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(ClientsEmails)
admin.site.register(ClientsPhones)
