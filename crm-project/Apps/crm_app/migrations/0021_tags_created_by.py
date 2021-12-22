# Generated by Django 3.2.9 on 2021-12-22 20:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crm_app', '0020_alter_clientsinfo_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='tags',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='users_app.users'),
            preserve_default=False,
        ),
    ]
