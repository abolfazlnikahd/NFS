# Generated by Django 4.2.4 on 2023-08-13 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FileSystem', '0001_initial'),
        ('pool', '0004_remove_volumegroup_host_remove_volumegroup_nfsshare_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='volumegroup',
            name='FileSystem',
        ),
        migrations.AddField(
            model_name='volumegroup',
            name='FileSystem',
            field=models.ManyToManyField(null=True, to='FileSystem.filesystem'),
        ),
    ]
