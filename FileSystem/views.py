from django.shortcuts import render , HttpResponse , get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from pool.models import VolumeGroup
from pool.views import validating_name
from .models import FileSystem
import os , subprocess , json



#---------------------------------------------- details ----------------------------------------------#
@csrf_exempt
def full_details(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        pool = request.POST.get('pool')
        size = request.POST.get('size')

        if validating_name(name) == False :
            return HttpResponse(f'<p> {name} is incorrect </p>')
        elif pool not in stringOfVolumeGroups():
            print(stringOfVolumeGroups())
            return HttpResponse(f'you dont have a pool with {pool} name ')
        
        ######## create lv
        lvExitCode = os.system(f'lvcreate -L {size}G -n {name} {pool}')
        if lvExitCode != 0:
            return HttpResponse(f'<p>Logical Volume "{name}" already exists in volume group "{pool}"</p>')
        ######## create filesystem
        mkfsExitCode = os.system(f'mkfs.ext4 /dev/{pool}/{name}')
        if mkfsExitCode != 0:
            os.system(f'lvremove /dev/{pool}/{name}')
            return HttpResponse("<p>file system didnt creat</p>")
        ######## save in db

        filesystem_db(name , pool)
        
        return HttpResponse("<p>file system created successfuly</p>")


    all = lvdisplay_response_list()
    responseDict = dict()
    LvNumber = 1
    for vg in all:
        vg = vg.split('\\n')
        temporaryList = list()
        for details in vg :
            if 'LV Name' in details:
                temporaryList.append(details[25::])
            if 'VG Name' in details:
                temporaryList.append(details[25::])
            if 'LV Size' in details:
                temporaryList.append(details[25::])
            if 'LV Status' in details:
                temporaryList.append(details[25::])

        responseDict[f'lv-{LvNumber}'] = ','.join(temporaryList)
        LvNumber += 1
        temporaryList.clear()
    #print(responseDict)
    
    return HttpResponse(json.dumps(responseDict))




#--------------------------------------------- remove ----------------------------------------------#
@csrf_exempt
def specifies_details(request , **kwargs):
    if request.method == 'DELETE':
        lvname = kwargs['lvname']
        if validating_name(lvname) == False :
            return HttpResponse(f'<p> {lvname} is incorrect </p>')

        lv = get_object_or_404(FileSystem,fileSystemName = lvname)
        if lv.NfsShare.all().count() != 0:
            return HttpResponse("<p>file system contain a nfs share</p>")
            
        os.system(f'wipefs -a {lv.lvpath}')
        os.system(f'yes | lvremove {lv.lvpath}')

        lv.delete()

        return HttpResponse("<p>file system successfuly removed</p>")
    return HttpResponse(status = 200)
#-----------------------------------------------------------------------------------------------------#

def lvdisplay_response_list():
    all = str(subprocess.Popen('lvdisplay' , stdout=subprocess.PIPE , shell=True).communicate()).split('--- Logical volume ---')
    all.remove(all[0])
    return all

def filesystem_db(lvname , vgname):
        fdb = FileSystem(fileSystemName = lvname,lvpath = f'/dev/{vgname}/{lvname}')#add file system to filesystem table
        fdb.save()

        db = VolumeGroup.objects.get(VgName = vgname)#file volume group 
        db.FileSystem.add(fdb)#add filesystem to volume group table
        db.save()    

def stringOfVolumeGroups():
    db = VolumeGroup.objects.all()
    temprorylist = list()
    for vg in db :
        temprorylist.append(vg.VgName)
    return ','.join(temprorylist)

def stringOfLogicalVolumes():
    db = FileSystem.objects.all()
    temprorylist = list()
    for lv in db:
        temprorylist.append(lv.fileSystemName)
    return ','.join(temprorylist)
