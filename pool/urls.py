from django.urls import path 
from .views import full_details , specifies_details

app_name = 'pool'

urlpatterns = [
    path('', full_details , name='details'),
    path('<str:vgname>' , specifies_details , name='remove')
]