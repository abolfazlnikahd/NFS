from django.shortcuts import render
import subprocess , shlex , os , re
from scripts import *

# Create your views here.
def vgs():
    return str(subprocess.Popen('vgs' , stdout=subprocess.PIPE , shell=True).communicate()[0]).split('\\n')

def details(request):
     
    
    allDetails  = vgs()
    allDetails.pop()
    print(allDetails)
     
    if len(allDetails) == 0:
        return render(request , 'pool/pooldetails.html' , {'msg':'no pool'})
    allDetails.remove(allDetails[0])
    for index in range(len(allDetails)):
        temporarylist= list()
        allDetails[index] = allDetails[index].strip().split(' ')
        for dataIndex in range(len(allDetails[index])):
            if allDetails[index][dataIndex] != '':
                temporarylist.append(allDetails[index][dataIndex]) 
        allDetails[index] = temporarylist.copy()

    print(allDetails)

    return render(request , 'pool/pooldetails.html' )





def addpool(request):
    if request.method == 'POST':
        vgname = request.POST.get('vgname')
        # start find available disk
        all =str(subprocess.Popen('lvmdiskscan | grep /dev/sd' , stdout=subprocess.PIPE , shell=True).communicate()[0]).split('\\n')
        all.pop()
        i = 0
        while i < len(all) :
            all[i] = (re.sub("\[.*?\]", "" , all[i])).strip()
            i+=1

        available = list()
        for i in all:
            if not str(i[-1]).isnumeric():
                available.append(i)
        #end finding available disk
        if len(available) > 0:
            i = 0
            while i < len(available):
                pvcreate = os.system(f'pvcreate {available[i]}')
                if i == len(available)-1 and pvcreate != 0:
                    return render(request , 'pool/pooldetails.html',{'msg':'you dont have a usable disk'})
                elif pvcreate == 0:
                    if os.system(f'vgcreate {vgname} {available[i]}') == 0:
                        return render(request , 'pool/pooldetails.html',{'msg':'pool successfuly created'})
                    os.system(f'pvremove {available[i]}')
                    return render(request , 'pool/pooldetails.html',{'msg':'name error'})
                i+=1
    return render(request , 'pool/add.html')

def remove(request):
    if request.method == 'POST':
        vgname = request.POST.get('vgname')
        pvpath = request.POST.get('pvpath')

        #start finding volume groups name and number of logical volume of them
        allVolumeGroupDetails = vgs()
        allVolumeGroupDetails.pop()
        allVolumeGroupDetails.remove(allVolumeGroupDetails[0])

        VGnames = dict()
        for details in allVolumeGroupDetails:
            splitedListOfDetails = str(details).strip().split(' ')
            VGnames[splitedListOfDetails[0]] = int(splitedListOfDetails[6])
        #end finding

        #start checking vg want to remove
        if VGnames[vgname] != 0:
            return render(request , 'pool/pooldetails.html' , {'msg':'your pool contain a file system please rmeove filesystem dirst'})
        #end checking

        #start deleting
        if os.system(f'vgremove {vgname}') == 0:
            if os.system(f'pvremove {pvpath}') == 0:
                return render(request , 'pool/pooldetails.html' , {'msg':'pool successfuly deleted'})
            os.system(f'vgcreate {vgname}')
            return render(request , 'pool/pooldetails.html' , {'msg':'pool not deleted'})
        return render(request , 'pool/pooldetails.html' , {'msg':'pool not deleted'})
        #end deleting
    return render(request , 'pool/remove.html')