
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from django.urls import reverse


class Users(AbstractUser):
    image = models.ImageField(upload_to='users_photo/', blank=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)

    def get_absolute_url(self):
        return reverse('user_detail', args=[str(self.id)])

    def __str__(self):
        return self.get_username()





