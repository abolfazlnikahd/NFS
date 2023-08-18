from django.shortcuts import render
from pool.models import VolumeGroup
from .models import FileSystem
import os , subprocess , json



#---------------------------------------------- details ----------------------------------------------#

def details(request):
    all = str(subprocess.Popen('lvdisplay' , stdout=subprocess.PIPE , shell=True).communicate()).split('--- Logical volume ---')
    all.remove(all[0])
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
    
    return render(request , 'Filesystem/details.html' , {'context' : json.dumps(responseDict)})




#---------------------------------------------- add -----------------------------------------------#
def add(request):
    pools = VolumeGroup.objects.all()
    if pools.count() == 0:
        return render(request , 'Filesystem/details.html' , {'msg':'you dont have a pool pleas create pool first'})

    if request.method == 'POST':
        name = request.POST.get('name')
        pool = request.POST.get('pool')
        size = request.POST.get('size')
        ######## create lv
        lv = os.system(f'lvcreate -L {size}G -n {name} {pool}')
        if lv != 0:
            return render(request , 'Filesystem/details.html' , {'msg':'this pool dont have free space you want'})
        ######## create filesystem
        mkfs = os.system(f'mkfs.ext4 /dev/{pool}/{name}')
        if mkfs != 0:
            os.system(f'lvremove /dev/{pool}/{name}')
            return render(request , 'Filesystem/details.html' , {'msg':'file system didnt creat'})
        ######## save in db
        fdb = FileSystem(fileSystemName = name,lvpath = f'/dev/{pool}/{name}')#add file system to filesystem table
        fdb.save()
        db = VolumeGroup.objects.filter(VgName = pool)#file volume group 
        for i in db:
            i.FileSystem.add(fdb)#add filesystem to volume group table
            i.save()
        
        return render(request , 'Filesystem/details.html' , {'msg':'file system created successfuly'})
    ########
    
    return render(request , 'Filesystem/add.html' , {'context':pools})


#--------------------------------------------- remove ----------------------------------------------#

def remove(request , lvname):
    lv = FileSystem.objects.get(fileSystemName = lvname)
    
    if lv.NfsShare == 'NfsShare.NfsShare.None':
        return render(request , 'Filesystem/details.html' , {'msg':'file system contain a nfs share'})
        
    os.system(f'wipefs -a {lv.lvpath}')
    os.system(f'yes | lvremove {lv.lvpath}')

    lv.delete()
    return render(request , 'Filesystem/details.html' , {'msg':'file system removed successfuly'})
    


