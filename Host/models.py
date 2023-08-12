from django.db import models

# Create your models here.
class Host(models.Model):
    Name = models.CharField(max_length=50 , unique=True)
    IpAddress = models.CharField(max_length=18 , unique=True)

    def __str__(self):
        return self.Name
    