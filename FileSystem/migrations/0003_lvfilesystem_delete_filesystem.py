# Generated by Django 4.2.4 on 2023-08-13 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pool', '0006_alter_volumegroup_filesystem'),
        ('Host', '0003_alter_host_ipaddress_alter_host_name'),
        ('FileSystem', '0002_alter_filesystem_host'),
    ]

    operations = [
        migrations.CreateModel(
            name='LvFileSystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fileSystemName', models.CharField(max_length=25)),
                ('NfsShare', models.TextField(blank=True, null=True, unique=True)),
                ('Host', models.ManyToManyField(blank=True, to='Host.host')),
            ],
        ),
        migrations.DeleteModel(
            name='FileSystem',
        ),
    ]
