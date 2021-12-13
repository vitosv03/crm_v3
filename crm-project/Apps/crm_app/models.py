from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from django.urls import reverse


class ClientsPhones(models.Model):
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,12}$")
    phoneNumber = models.CharField(validators=[phoneNumberRegex], max_length=13, help_text='e.g. +380991234567')
    client = models.ForeignKey('ClientsInfo', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.phoneNumber


class ClientsEmails(models.Model):
    email = models.EmailField(max_length=100)
    client = models.ForeignKey('ClientsInfo', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.email


class ClientsInfo(models.Model):
    title = models.CharField(max_length=100)
    head = models.CharField(max_length=100)
    summary = models.TextField()
    address = models.CharField(max_length=100)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)

    def display_phoneNumber(self):
        return ", ".join([phone.phoneNumber for phone in self.clientsphones_set.all()])

    def display_email(self):
        return ", ".join([e.email for e in self.clientsemails_set.all()])

    def get_absolute_url(self):
        return reverse('ClientDetail', args=[str(self.id)])

    def __str__(self):
        return self.title


class ProjectsList(models.Model):
    client = models.ForeignKey('ClientsInfo', on_delete=models.CASCADE)
    p_name = models.CharField(max_length=100)
    description = models.TextField()
    date_begin = models.DateField()
    date_end = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)

    def get_absolute_url(self):
        return reverse('ProjectDetail', args=[str(self.id)])

    def __str__(self):
        return self.p_name


class Tags(models.Model):
    tag = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.tag


class InterPlaysList(models.Model):
    project = models.ForeignKey('ProjectsList', on_delete=models.CASCADE)
    link_status = (('cl', 'by claim'), ('le', 'by letter'), ('si', 'by site'), ('co', 'by company'),)
    link = models.CharField(max_length=2, choices=link_status, blank=True, default=None, help_text='select link')
    description = models.TextField()
    rating = models.IntegerField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)
    tag = models.ManyToManyField(Tags)

    def get_client(self):
        return ClientsInfo.objects.filter(projectslist__p_name=self.project)[0]

    def get_link(self):
        return self.get_link_display()

    def get_tag(self):
        return ', '.join([tag.tag for tag in self.tag.all()])

    def get_absolute_url(self):
        return reverse('InterplayDetail', args=[str(self.id)])

    def __str__(self):
        return str(self.project)
