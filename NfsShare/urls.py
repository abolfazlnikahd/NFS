from django.urls import path 
from .views import full_details , specifies_details

app_name = 'NfsShare'
urlpatterns = [
    path('' , full_details , name='details'),
    path('<str:nfsname>' , specifies_details , name='remove'),
]
