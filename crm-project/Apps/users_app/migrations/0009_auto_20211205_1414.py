# Generated by Django 3.2.9 on 2021-12-05 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0008_clientsemails_clientsinfo_clientsphones'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientsinfo',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='clientsinfo',
            name='email',
        ),
        migrations.RemoveField(
            model_name='clientsinfo',
            name='phoneNumber',
        ),
        migrations.DeleteModel(
            name='ClientsEmails',
        ),
        migrations.DeleteModel(
            name='ClientsInfo',
        ),
        migrations.DeleteModel(
            name='ClientsPhones',
        ),
    ]
