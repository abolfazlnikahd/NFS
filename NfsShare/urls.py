from django.urls import path 
from .views import *

app_name = 'NfsShare'
urlpatterns = [
    path('' , details , name='details'),
    path('add' , add , name='add'),
    path('<str:nfsname>/remove' , remove , name='remove'),
]
