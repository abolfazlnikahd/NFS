from django.db import models
from NfsShare.models import NfsShare
# Create your models here.
class FileSystem(models.Model):
    fileSystemName = models.CharField(max_length=25 , unique=True)
    lvpath = models.CharField(max_length=100 , null=True)
    NfsShare = models.ManyToManyField(NfsShare,blank=True)

    def  __str__(self):
        return self.fileSystemName
    