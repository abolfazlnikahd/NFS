from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pools/' , include('pool.urls')),
    path('Hosts/' , include('Host.urls')),
    path('Filesystems/' , include('FileSystem.urls')),
    path('NfsShares/' , include('NfsShare.urls'))

]
