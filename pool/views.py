from django.shortcuts import render , HttpResponse
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

    return HttpResponse(status = 200)



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
                    return HttpResponse("<p>you dont have a usable disk</p>")
                elif pvcreate == 0:
                    if os.system(f'vgcreate {vgname} {available[i]}') == 0:
                        db = VolumeGroup(PvPath = available[i] , VgName = vgname)
                        db.save()
                        return HttpResponse("<p>pool successfuly created</p>")
                    os.system(f'pvremove {available[i]}')
                    return HttpResponse("<p>name error</p>")
                i+=1
    return HttpResponse(status=201)


#---------------------------------------------remove-------------------------------------------#   

def remove(request , vgname):


        query = VolumeGroup.objects.get(VgName = vgname)
        pvpath = query.PvPath
        if query.FileSystem == 'FileSystem.FileSystem.None':
            return HttpResponse("<p>your pool contain a file system</p>")
        #start deleting
        if os.system(f'vgremove {vgname}') == 0:
            if os.system(f'pvremove {pvpath}') == 0:
                db = VolumeGroup.objects.get(VgName = vgname)
                db.delete()
                return HttpResponse("<p>pool successfuly deleted</p>")  
            os.system(f'vgcreate {vgname}')
            return HttpResponse("<p></p>")  
        return HttpResponse("<p>pool not deleted</p>") 
        #end deleting
    