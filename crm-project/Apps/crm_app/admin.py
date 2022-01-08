from django import forms
from django.contrib import admin
from django.utils.translation import gettext, gettext_lazy as _
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from .models import ClientsInfo, ClientsEmails, ClientsPhones, ProjectsList, Tags, InterPlaysList


# Register your models here.

class ClientsInfoAdminForm(forms.ModelForm):
    """
    Change field summary for working ckeditor in admin module
    """
    summary = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = ClientsInfo
        fields = '__all__'


class ClientsEmailsInline(admin.TabularInline):
    """
    add ClientsEmails to TabularInline
    """
    model = ClientsEmails
    extra = 0


class ClientsPhonesInline(admin.TabularInline):
    """
    add ClientsPhones to TabularInline
    """
    model = ClientsPhones
    extra = 0


@admin.register(ClientsEmails)
class ClientsEmailsAdmin(admin.ModelAdmin):
    """
    add ClientsEmails to admin
    """
    list_display = ('email', 'client', 'date_created', 'date_updated',)


@admin.register(ClientsPhones)
class ClientsPhonesAdmin(admin.ModelAdmin):
    """
    add ClientsPhones to admin
    """
    list_display = ('phoneNumber', 'client', 'date_created', 'date_updated',)


@admin.register(ClientsInfo)
class ClientsInfoAdmin(admin.ModelAdmin):
    """
    add ClientsInfo to admin and config it
    """
    form = ClientsInfoAdminForm

    list_display = ('title', 'head', 'summary', 'created_by',
                    'display_phoneNumber', 'display_email', 'date_created', 'date_updated',)

    inlines = [ClientsEmailsInline, ClientsPhonesInline, ]
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

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        # obj.email = ", ".join([e.email for e in obj.clientsemails_set.all()])
        # obj.phone = ", ".join([phone.phoneNumber for phone in obj.clientsphones_set.all()])
        super().save_model(request, obj, form, change)


@admin.register(ProjectsList)
class ProjectsListAdmin(admin.ModelAdmin):
    """
    add ProjectsList to admin and config it
    """
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
    """
    add Tags to admin and config it
    """
    list_display = ('tag', 'date_created', 'date_updated',)
    readonly_fields = ('date_created', 'date_updated',)


@admin.register(InterPlaysList)
class InterPlaysAdmin(admin.ModelAdmin):
    """
    add InterPlays to admin and config it
    """
    list_display = ('project', 'link', 'date_created', 'date_updated', 'client')

    readonly_fields = ('date_created', 'date_updated', 'created_by')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        # obj.modified_by = request.user
        obj.client = ClientsInfo.objects.filter(
            projectslist__p_name=obj.project).values_list('title', flat=True)[0]
        super().save_model(request, obj, form, change)
