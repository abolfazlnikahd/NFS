from django.contrib import admin
from django.urls import path , include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('pools/' , include('pool.urls')),
    path('Hosts/' , include('Host.urls')),

]
