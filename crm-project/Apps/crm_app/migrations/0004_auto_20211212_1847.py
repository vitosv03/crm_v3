# Generated by Django 3.2.9 on 2021-12-12 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0003_projectslist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectslist',
            name='date_begin',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='projectslist',
            name='date_end',
            field=models.DateField(),
        ),
    ]
