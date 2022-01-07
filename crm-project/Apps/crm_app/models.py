from ckeditor.fields import RichTextField
from django.conf import settings
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.
from django.urls import reverse
from .utils import link_status_InterPlaysListModel


class ClientsPhones(models.Model):
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,12}$")
    phoneNumber = models.CharField(validators=[phoneNumberRegex], max_length=13, help_text='e.g. +380991234567')
    client = models.ForeignKey('ClientsInfo', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        verbose_name = 'ClientsPhones'
        verbose_name_plural = 'ClientsPhones'
        ordering = ['-date_created']

    def __str__(self):
        return self.phoneNumber


class ClientsEmails(models.Model):
    email = models.EmailField(max_length=100)
    client = models.ForeignKey('ClientsInfo', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        verbose_name = 'ClientsEmails'
        verbose_name_plural = 'ClientsEmails'
        ordering = ['-date_created']

    def __str__(self):
        return self.email


class ClientsInfo(models.Model):
    is_active = models.BooleanField(default=True)
    title = models.CharField(max_length=100)
    head = models.CharField(max_length=100)
    summary = RichTextField(blank=True, null=True)
    address = models.CharField(max_length=100)
    email = models.TextField(blank=True)
    phone = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)

    # def display_phoneNumber(self):
    #     return ", ".join([phone.phoneNumber for phone in self.clientsphones_set.all()])
    #
    # def display_email(self):
    #     return ", ".join([e.email for e in self.clientsemails_set.all()])

    def get_absolute_url(self):
        return reverse('client_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        self.email = ", ".join([e.email for e in self.clientsemails_set.all()])
        self.phone = ", ".join([phone.phoneNumber for phone in self.clientsphones_set.all()])
        super(ClientsInfo, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'ClientsInfo'
        verbose_name_plural = 'ClientsInfo'
        ordering = ['-date_created']
        # permissions = (("clients_info_edit", "Edit Client Information"),)

    def __str__(self):
        return self.title


class ProjectsList(models.Model):
    is_active = models.BooleanField(default=True)
    client = models.ForeignKey('ClientsInfo', on_delete=models.CASCADE)
    p_name = models.CharField(max_length=100)
    description = models.TextField()
    date_begin = models.DateField()
    date_end = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)

    def get_absolute_url(self):
        return reverse('project_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'ProjectsList'
        verbose_name_plural = 'ProjectsList'
        ordering = ['-date_created']

    def __str__(self):
        return self.p_name


class Tags(models.Model):
    tag = models.CharField(max_length=20)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)

    def get_absolute_url(self):
        return reverse('tag_detail', args=[str(self.id)])

    class Meta:
        verbose_name = 'Tags'
        verbose_name_plural = 'Tags'
        ordering = ['-date_created']

    def __str__(self):
        return self.tag


class InterPlaysList(models.Model):
    is_active = models.BooleanField(default=True)
    project = models.ForeignKey('ProjectsList', on_delete=models.CASCADE)
    link = models.CharField(max_length=2, choices=link_status_InterPlaysListModel, blank=True, default=None, help_text='select link')
    description = models.TextField()
    rating = models.SmallIntegerField(validators=[MinValueValidator(-5), MaxValueValidator(5)])
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)
    tag = models.ManyToManyField(Tags)
    client = models.CharField(max_length=100, blank=True)

    def get_absolute_url(self):
        return reverse('interplay_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        self.client = ClientsInfo.objects.filter(
            projectslist__p_name=self.project).values_list('title', flat=True)[0]
        super(InterPlaysList, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'InterPlaysList'
        verbose_name_plural = 'InterPlaysList'
        ordering = ['-date_created']

    def __str__(self):
        return str(self.project)
