# Generated by Django 4.2.4 on 2023-08-12 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Host', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='host',
            old_name='ipAddress',
            new_name='IpAddress',
        ),
        migrations.RenameField(
            model_name='host',
            old_name='name',
            new_name='Name',
        ),
    ]
