from django.contrib import admin
from .models import ClientsInfo, ClientsEmails, ClientsPhones
# Register your models here.


admin.site.register(ClientsInfo)
admin.site.register(ClientsEmails)
admin.site.register(ClientsPhones)
