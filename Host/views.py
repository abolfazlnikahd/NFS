from django.shortcuts import render
from .models import *

# Create your views here.

def details(request):
    detail = Host.objects.all()
    
    return render(request , 'Host/details.html' , {'detail':detail})

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

        return render(request , 'Host/details.html' , {'msg':msg})
        

    return render(request , 'Host/add.html')

def remove(request , name):
    client = Host.objects.filter(Name = name)
    clientCount = client.count()
    if clientCount  == 0:
        msg ='sorry no such Host found!'

    for i in client:
        i.delete()
        msg = 'Host removed successfuly '
    return render(request , 'Host/details.html' , {'msg':msg})