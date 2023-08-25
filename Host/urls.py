from django.urls import path 
from .views import * 

app_name = 'Host'

urlpatterns = [
    path('' , details , name='details'),
    path('<str:name>' , remove , name='remove')

]
