from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models


# Create your models here.
from django.urls import reverse


class ClientsPhones(models.Model):
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,12}$")
    phoneNumber = models.CharField(validators=[phoneNumberRegex], max_length=13, unique=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.phoneNumber


class ClientsEmails(models.Model):
    email = models.EmailField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.email


class ClientsInfo(models.Model):
    title = models.CharField(max_length=100)
    head = models.CharField(max_length=100)
    summary = models.TextField()
    address = models.CharField(max_length=100)
    phoneNumber = models.ManyToManyField(ClientsPhones, help_text='e.g. +380991234567')
    email = models.ManyToManyField(ClientsEmails, help_text='e.g. mail@test.com')
    # created_by = models.CharField(max_length=100, default=request.user)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)

    def display_phoneNumber(self):
        return ', '.join([phoneNumber.phoneNumber for phoneNumber in self.phoneNumber.all()])

    def display_email(self):
        return ', '.join([email.email for email in self.email.all()])


    def get_absolute_url(self):
        return reverse('client-detail', args=[str(self.id)])

    def __str__(self):
        return self.title
