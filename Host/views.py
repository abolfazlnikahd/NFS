import json , ipaddress , subprocess
from django.shortcuts import render , HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pool.views import validating_name

from .models import *

# Create your views here.

#-------------------------------------details--------------------------------#
@csrf_exempt
def details(request):
    # add host
    if request.method == 'POST':
        hostName= request.POST.get('hostName')
        if validating_name(hostName) == False:
            return HttpResponse(f'<p> {hostName} is incorrect</p>')
        ipAddress = request.POST.get('ipAddress')
        exitCode_ipValidations = validating_ipaddress(ipAddress)
        if exitCode_ipValidations == 1 :
            return HttpResponse(f"<p>{ipAddress} in not valid</p>")
        elif exitCode_ipValidations == 2: #single ip
            if '0% packet loss' not in str(subprocess.Popen(f'ping -c 1 {ipAddress}' , stdout=subprocess.PIPE , shell=True).communicate()):
                return HttpResponse(f"<p>we don't have access to {ipAddress}</p>")
            ipAddress = str(ipAddress) + '/32'
        
        try:
            client = Host(Name = hostName ,IpAddress = ipAddress)
            client.save()
            msg = 'host successfuly added'
        except:
            msg = 'name or ipaddress alredy used pleas try again'

        return HttpResponse(f"<p>{msg}</p>")
    # end add host

    detail = Host.objects.all()
    flag = 1
    responsedict = dict()
    for i in detail:
        responsedict[f'Host-{flag}']= str(i.Name) + '   ' +str(i.IpAddress)
        flag += 1
    return HttpResponse(json.dumps(responsedict))



#-------------------------------------remove---------------------------------#
@csrf_exempt
def remove(request , name):
    if validating_name(name) == False:
        return HttpResponse(f'<p> {name} is incorrect</p>')
    if request.method == 'DELETE':
        try:
            client = Host.objects.get(Name = name)
            client.delete()
            return HttpResponse("<p>Host removed successfuly </p>")
        except :
            return HttpResponse('<p>Host does not exist</p>')
    return HttpResponse(status = 200)   


#-----------------------------------------------------------------------------#
def validating_ipaddress(ipAddress):
    if '/' in ipAddress:
        ipSplit = str(ipAddress).split('/')
        try:
            ipaddress.ip_address(ipSplit[0])
            if int(ipSplit[1]) > 32 and int(ipSplit[1]) < 0:
                return 1
            return 0
        except ValueError:
            return 1

    try:
        ipaddress.ip_address(ipAddress)
        return 2  #single ip
    except:
        return 1