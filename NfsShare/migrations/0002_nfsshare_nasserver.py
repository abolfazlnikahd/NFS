# Generated by Django 4.2.4 on 2023-08-18 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NfsShare', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nfsshare',
            name='NasServer',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
