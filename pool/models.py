from django.db import models
from FileSystem.models import FileSystem


# Create your models here.
class VolumeGroup(models.Model):
    PvPath = models.TextField()
    VgName = models.CharField(max_length=30 , unique=True)
    FileSystem = models.ManyToManyField( FileSystem , blank=True)

    def __str__(self):
        return self.VgName

