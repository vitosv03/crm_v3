from django.db import models


# Create your models here.

class Manager(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=50, help_text=' ex. name@gmail.com')
    image = models.ImageField(upload_to='managers_images/', default='managers_images/manager_icon.png')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class OtherUser(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=50, help_text=' ex. name@gmail.com')
    image = models.ImageField(upload_to='users_images/', default='users_images/user_icon.png')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + ' ' + self.last_name
