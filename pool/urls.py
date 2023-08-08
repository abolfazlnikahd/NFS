from django.urls import path 
from .views import *

app_name = 'pool'

urlpatterns = [
    path('', details , name='details'),
    path('add' , addpool , name='add' ),
    path('remove' , remove , name='remove')
]