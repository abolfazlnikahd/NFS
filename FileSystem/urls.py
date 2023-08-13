from django.urls import path 
from .views import *

app_name = 'Filesystem'
urlpatterns = [
    path('' , details , name='details'),
    path('add' , add , name='add'),
    path('<str:lvname>/remove' , remove , name='remove'),
]
