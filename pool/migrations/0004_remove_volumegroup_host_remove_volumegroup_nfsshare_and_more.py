# Generated by Django 4.2.4 on 2023-08-13 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FileSystem', '0001_initial'),
        ('pool', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='volumegroup',
            name='Host',
        ),
        migrations.RemoveField(
            model_name='volumegroup',
            name='NfsShare',
        ),
        migrations.AlterField(
            model_name='volumegroup',
            name='FileSystem',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='FileSystem.filesystem', unique=True),
        ),
    ]