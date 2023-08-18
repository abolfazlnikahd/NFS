from django.shortcuts import render
import subprocess , shlex , os , re , json
from .models import VolumeGroup

# Create your views here.
def vgs():
    return str(subprocess.Popen('vgs' , stdout=subprocess.PIPE , shell=True).communicate()[0]).split('\\n')

#---------------------------------------------details--------------------------------------------#
def details(request):
     
    
    allDetails  = vgs()
    allDetails.pop()
    #print(allDetails)
     
    if len(allDetails) == 0:
        return render(request , 'pool/pooldetails.html' , {'msg':'no pool'})
    allDetails.remove(allDetails[0])
    responsedict = dict()
    flag = 1
    for vgindex in range(len(allDetails)):
        responsedict[f'vg-{flag}'] = allDetails[vgindex]
        flag += 1
    """ 
    for index in range(len(allDetails)):
        temporarylist= list()
        allDetails[index] = allDetails[index].strip().split(' ')
        for dataIndex in range(len(allDetails[index])):
            if allDetails[index][dataIndex] != '':
                temporarylist.append(allDetails[index][dataIndex]) 
        allDetails[index] = temporarylist.copy()
        response = json.dumps(allDetails)
    """

    responsedict = json.dumps(responsedict)

    return render(request , 'pool/pooldetails.html' ,{'context':responsedict})



#---------------------------------------------add------------------------------------------#


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
                        db = VolumeGroup(PvPath = available[i] , VgName = vgname)
                        db.save()
                        return render(request , 'pool/pooldetails.html',{'msg':'pool successfuly created'})
                    os.system(f'pvremove {available[i]}')
                    return render(request , 'pool/pooldetails.html',{'msg':'name error'})
                i+=1
    return render(request , 'pool/add.html')


#---------------------------------------------remove-------------------------------------------#

def remove(request , vgname):


        query = VolumeGroup.objects.get(VgName = vgname)
        pvpath = query.PvPath
        if query.FileSystem == 'FileSystem.FileSystem.None':
            return render(request , 'pool/pooldetails.html' , {'msg':'your pool contain a file system'})
        #start deleting
        if os.system(f'vgremove {vgname}') == 0:
            if os.system(f'pvremove {pvpath}') == 0:
                db = VolumeGroup.objects.get(VgName = vgname)
                db.delete()
                return render(request , 'pool/pooldetails.html' , {'msg':'pool successfuly deleted'})
            os.system(f'vgcreate {vgname}')
            return render(request , 'pool/pooldetails.html' , {'msg':'pool not deleted'})
        return render(request , 'pool/pooldetails.html' , {'msg':'pool not deleted'})
        #end deleting
    