from django.db import models
from Host.models import Host
# Create your models here.
class FileSystem(models.Model):
    fileSystemName = models.CharField(max_length=25 , unique=True)
    lvpath = models.CharField(max_length=100 , null=True)
    NfsShare = models.TextField(null=True,blank=True,unique=True)
    Host = models.ManyToManyField(Host , blank=True)

    def  __str__(self):
        return self.fileSystemName
    