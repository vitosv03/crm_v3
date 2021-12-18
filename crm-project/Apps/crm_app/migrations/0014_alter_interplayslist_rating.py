# Generated by Django 3.2.9 on 2021-12-18 20:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0013_interplayslist_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interplayslist',
            name='rating',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(-5), django.core.validators.MinValueValidator(5)]),
        ),
    ]
