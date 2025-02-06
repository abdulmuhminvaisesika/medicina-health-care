# Generated by Django 5.1.5 on 2025-01-28 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0002_customuser_address_delete_useraddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='role',
            field=models.CharField(blank=True, choices=[('Customer', 'Customer'), ('Owner', 'Owner')], default='Customer', max_length=10),
        ),
    ]
