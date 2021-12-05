from django import forms
from django.forms import ModelForm
from .models import ClientsInfo, ClientsEmails, ClientsPhones


class ClientsInfoForm(ModelForm):
    # DEMO_CHOICES = (
    #     ("+380995555555", "+380995555555"),
    #     ("+380995555556", "+380995555556"),
    # )
    email = forms.ModelMultipleChoiceField(queryset=ClientsEmails.objects.all())
    phoneNumber = forms.ModelMultipleChoiceField(queryset=ClientsPhones.objects.all())
    # phoneNumber = forms.MultipleChoiceField(choices=DEMO_CHOICES)

    class Meta:
        model = ClientsInfo
        fields = ['title', 'head', 'summary', 'address', 'phoneNumber', 'email', 'created_by']
        # fields = '__all__'

#
# title = models.CharField(max_length=100)
#    head = models.CharField(max_length=100)
#    summary = models.TextField()
#    address = models.CharField(max_length=100)
#    phoneNumber = models.ManyToManyField(ClientsPhones, help_text='e.g. +380991234567')
#    email = models.ManyToManyField(ClientsEmails, help_text='e.g. mail@test.com')
#    # created_by = models.CharField(max_length=100, default=request.user)
#    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#    date_created = models.DateTimeField(auto_now_add=True, blank=True)
#    date_updated = models.DateTimeField(auto_now=True, blank=True)
