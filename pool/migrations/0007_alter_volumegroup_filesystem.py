# Generated by Django 4.2.4 on 2023-08-13 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FileSystem', '0003_lvfilesystem_delete_filesystem'),
        ('pool', '0006_alter_volumegroup_filesystem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volumegroup',
            name='FileSystem',
            field=models.ManyToManyField(blank=True, to='FileSystem.lvfilesystem'),
        ),
    ]