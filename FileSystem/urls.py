from django.urls import path 
from .views import full_details , specifies_details

app_name = 'Filesystem'
urlpatterns = [
    path('' , full_details , name='details'),
    path('<str:lvname>' , specifies_details , name='remove'),
]
