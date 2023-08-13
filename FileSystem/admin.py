from django.contrib import admin
from .models import FileSystem



# Register your models here.ad
@admin.register(FileSystem)
class FileSystemAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = ['id' , 'fileSystemName']