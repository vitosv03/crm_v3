from django.db import models
from django.contrib.auth.models import AbstractUser


#
# # Create your models here.

class Users(AbstractUser):
    image = models.ImageField(upload_to='users_photo/', blank=True)

    def __str__(self):
        return self.username
