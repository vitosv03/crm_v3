# Generated by Django 3.2.9 on 2021-12-18 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0012_remove_interplayslist_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='interplayslist',
            name='client',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
