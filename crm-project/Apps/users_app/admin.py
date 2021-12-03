from django.contrib import admin

# Register your models here.
from .models import Manager, OtherUser

admin.site.register(Manager)
admin.site.register(OtherUser)
