from django.db import models
from Host.models import Host

# Create your models here.
class NfsShare(models.Model):
    Name  = models.CharField(max_length=25)
    mountPoint = models.CharField(max_length=100)
    NasServer = models.CharField(max_length=100 , null=True)
    Host = models.OneToOneField(Host , on_delete=models.CASCADE )

    def __str__(self):
        return self.Name 