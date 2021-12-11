# from django import forms
# from django.forms import ModelForm
# from .models import ClientsInfo, ClientsEmails, ClientsPhones
#
#
# class ClientsInfoForm(ModelForm):
#     # DEMO_CHOICES = (
#     #     ("+380993333333", "+380993333333"),
#     #     ("+380993333336", "+380993333336"),
#     # )
#     # email = forms.ModelMultipleChoiceField(queryset=ClientsEmails.objects.all())
#     # phoneNumber = forms.ModelMultipleChoiceField(queryset=ClientsPhones.objects.all())
#     # phoneNumber = forms.MultipleChoiceField(choices=DEMO_CHOICES)
#
#     class Meta:
#         model = ClientsInfo
#         fields = ['title', 'head', 'summary', 'address', 'email']
#         # fields = ['title', 'head', 'summary', 'address', 'phoneNumber', 'email', 'created_by']
#         # fields = '__all__'
#
