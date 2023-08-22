from django.shortcuts import render , HttpResponse
from .models import *

# Create your views here.

#-------------------------------------details--------------------------------#
def details(request):
    detail = Host.objects.all()
    
    return HttpResponse(status = 200)



#-------------------------------------add-----------------------------------#
def addHost(request):
    if request.method == 'POST':
        hostName= request.POST.get('hostName')
        ipAddress = request.POST.get('ipAddress')
        try:
            client = Host(Name = hostName ,IpAddress = ipAddress)
            client.save()
            msg = 'host successfuly added'
        except:
            msg = 'name or ipaddress alredy used pleas try again'

        return HttpResponse(f"<p>{msg}</p>")
        

    return HttpResponse(status = 200)


#-------------------------------------remove---------------------------------#
def remove(request , name):
    client = Host.objects.get(Name = name)
    clientCount = client.count()
    if clientCount  == 0:
        msg ='sorry no such Host found!'
        return HttpResponse(f"<p>{msg}</p>")
    client.delete()
    msg = 'Host removed successfuly '
    return HttpResponse(f"<p>{msg}</p>")