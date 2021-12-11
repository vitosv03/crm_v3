from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from .models import ClientsInfo, ClientsPhones, ClientsEmails


class ClientsInfoForm(ModelForm):
    class Meta:
        model = ClientsInfo
        fields = '__all__'


ClientsPhonesFormSet = inlineformset_factory(ClientsInfo, ClientsPhones, fields=('phoneNumber',), extra=1, can_delete=False, can_order=False)
ClientsEmailsFormSet = inlineformset_factory(ClientsInfo, ClientsEmails,   fields=('email',), extra=1, can_delete=False, can_order=False)
