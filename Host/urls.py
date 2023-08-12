from django.urls import path 
from .views import * 

app_name = 'Host'

urlpatterns = [
    path('' , details , name='details'),
    path('add' , addHost , name='add'),
    path('<str:name>/remove' , remove , name='remove')

]
