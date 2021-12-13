from django.contrib import admin
from django.utils.translation import gettext, gettext_lazy as _

from .models import ClientsInfo, ClientsEmails, ClientsPhones, ProjectsList, Tags, InterPlaysList


# Register your models here.

class ClientsEmailsInline(admin.TabularInline):
    model = ClientsEmails
    extra = 0


class ClientsPhonesInline(admin.TabularInline):
    model = ClientsPhones
    extra = 0


@admin.register(ClientsEmails)
class ClientsEmailsAdmin(admin.ModelAdmin):
    list_display = ('email', 'client', 'date_created', 'date_updated',)


@admin.register(ClientsPhones)
class ClientsPhonesAdmin(admin.ModelAdmin):
    list_display = ('phoneNumber', 'client', 'date_created', 'date_updated',)


@admin.register(ClientsInfo)
class ClientsInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'head', 'summary', 'created_by',
                    'display_phoneNumber', 'display_email', 'date_created', 'date_updated', )
    inlines = [ClientsEmailsInline, ClientsPhonesInline,]
    extra = 1

    fieldsets = (
        (None, {'fields': ('title', 'head', 'summary')}),
        (_('Created_by'), {'fields': ('created_by',)}),
        (_('Dates'), {'fields': ('date_created', 'date_updated')}),
    )

    readonly_fields = ('date_created', 'date_updated', 'created_by')

    add_fieldsets = (
        (None, {'fields': ('title', 'head',)}),
    )

    # def phoneNumber(self, obj):
    #     return ", ".join([phone.phoneNumber for phone in obj.clientsphones_set.all()])

    # def email(self, obj):
    #     return ", ".join([e.email for e in obj.clientsemails_set.all()])

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        # obj.modified_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ProjectsList)
class ProjectsListAdmin(admin.ModelAdmin):
    list_display = ('client', 'p_name', 'description', 'date_begin', 'date_end', 'value',
                    'created_by', 'date_created', 'date_updated',)

    readonly_fields = ('date_created', 'date_updated', 'created_by')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        # obj.modified_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('tag', 'date_created', 'date_updated',)
    readonly_fields = ('date_created', 'date_updated', )


@admin.register(InterPlaysList)
class InterPlaysAdmin(admin.ModelAdmin):
    list_display = ('project', 'link', 'date_created', 'date_updated', 'get_client')


    readonly_fields = ('date_created', 'date_updated', 'created_by')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        # obj.modified_by = request.user
        super().save_model(request, obj, form, change)












