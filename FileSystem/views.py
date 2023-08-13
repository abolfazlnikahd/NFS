from django.shortcuts import render
from pool.models import VolumeGroup
from .models import FileSystem
import os 



#---------------------------------------------- details ----------------------------------------------#

def details(request):
    ob = FileSystem.objects.all()
    
    return render(request , 'Filesystem/details.html' , {'context' : ob})




#---------------------------------------------- add -----------------------------------------------#
def add(request):
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
    return render(request , 'Filesystem/add.html')


#--------------------------------------------- remove ----------------------------------------------#

def remove(request , lvname):
    lv = FileSystem.objects.filter(fileSystemName = lvname)
    for i in lv:
        if i.NfsShare != None:
            return render(request , 'Filesystem/details.html' , {'msg':'file system contain a nfs share'})
        
        os.system(f'wipefs -a {i.lvpath}')
        os.system(f'yes | lvremove {i.lvpath}')

        lv.delete()
        return render(request , 'Filesystem/details.html' , {'msg':'file system removed successfuly'})
    