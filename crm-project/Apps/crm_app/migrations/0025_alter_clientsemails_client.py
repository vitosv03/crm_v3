# Generated by Django 3.2.9 on 2021-12-26 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0024_alter_clientsemails_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientsemails',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_app.clientsinfo'),
        ),
    ]
