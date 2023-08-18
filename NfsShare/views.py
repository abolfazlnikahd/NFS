from django.shortcuts import render
import os 
from pool.models import VolumeGroup
from FileSystem.models import FileSystem
from Host.models import Host
from .models import NfsShare
# Create your views here.

def addrolback(nfspath):
    os.system(f'umount {nfspath}')
    os.system(f"sed -i '/{nfspath}/d' /etc/exports ")
    os.system(f'rm -r {nfspath}')
    os.system('exportfs -a')
    os.system('systemctl restart nfs-kernel-srver')

#functions used in views ^    
#---------------------------------------------details-----------------------------------------------#

def details(request):
    details = NfsShare.objects.all()

    return render(request , 'NfsShare/details.html' , {'context':details})



#---------------------------------------------add---------------------------------------------------#

def add(request):
    #default path : /NfsShares
    if request.method == 'POST':
        folderName  = request.POST.get('folderName')
        fileSystemName = request.POST.get('fileSystem')
        host = request.POST.get('host')
        server = request.POST.get('server') 


        fileSystemPath = FileSystem.objects.get(fileSystemName = fileSystemName).lvpath
        hostIp = Host.objects.get(Name = host).IpAddress

        folderpath = f'/NfsShares/{folderName}'
        os.system('cp /etc/expots /project/nfsproject/exportsbackup')
        if os.system(f'mkdir -p {folderpath}') == 0:
            if os.system(f'chmod 770 {folderpath}') == 0:
                if os.system(f'mount {fileSystemPath} {folderpath}') == 0:
                    if os.system(f'echo "{folderpath} {hostIp}(rw,sync,no_subtree_check)" >> /etc/exports'):
                        if os.system('exportfs -a') == 0:
                            if os.system('systemctl restart nfs-kernel-server') == 0:
                                if os.system(f'ufw allow from {hostIp} to any port nfs') == 0:
                                    if os.system('ufw enable') == 0:
                                        db = NfsShare(Name = folderName , mountPoint = folderpath , Host = Host.objects.get(Name = host))
                                        db.save()
                                        return render(request , 'NfsShare/details.html' , {'msg':'your NFS share successfuly crated'})
                                    addrolback(folderpath)
                                    return render(request , 'NfsShare/details.html' , {'msg':'nfs share did not created'})
                                addrolback(folderpath)
                                return render(request , 'NfsShare/details.html' , {'msg':'nfs share did not created'})
                            addrolback(folderpath)
                            return render(request , 'NfsShare/details.html' , {'msg':'nfs share did not created'})
                        addrolback(folderpath)
                        return render(request , 'NfsShare/details.html' , {'msg':'nfs share did not created'})
                    os.system(f'umount {folderpath}')
                    os.system(f'rm -r {folderpath}')
                    return render(request , 'NfsShare/details.html' , {'msg':'nfs share did not created'})
                os.system(f'rm -r {folderpath}')
                return render(request , 'NfsShare/details.html' , {'msg':'nfs share did not created'})
            os.system(f'rm -r {folderpath}')
            return render(request , 'NfsShare/details.html' , {'msg':'nfs share did not created'})
        #print(folderName + poolName + fileSystemName + host)
        return render(request , 'NfsShare/details.html')
    
    
    #check pool
    pool_filesystem = VolumeGroup.objects.all()
    if pool_filesystem.count() == 0:
        return render(request , 'NfsShare/details.html' , {'msg':'you dont have any pool pleas create a pool and file system first'})
    
    #check file system 
    getResponse = dict()
    for pool in pool_filesystem:
        temproryList = list()
        for filesystem in  pool.FileSystem.distinct():
            temproryList.append(str(filesystem))
        if  ','.join(temproryList) == '':
            continue
        getResponse[pool.VgName] = ','.join(temproryList)

    if getResponse == {}:
        return render(request , 'NfsShare/details.html' , {'msg':'you dont have any filesystem pleas create file system first'})

    #check Host 
    if Host.objects.all().count() == 0:
        return render(request , 'NfsShare/details.html' , {'msg':'you dont have any host pleas create host'})



    return render(request , 'NfsShare/add.html' , {'context' : getResponse})





#---------------------------------------------remove-------------------------------------------------#

def remove(request , nfsname):
    nfspath = f'/NfsShares/{nfsname}'
    os.system(f'umount {nfspath}')
    os.system(f"sed -i '/{nfspath}/d' /etc/exports")
    os.system(f'rm -r {nfspath}')
    os.system('exportfs -a')
    os.system('systemctl restart nfs-kernel-server')
    db = NfsShare.objects.get(Name = nfsname)
    db.delete()
    return render(request , 'Nfsshare/details.html' , {'msg':'NFS share successfuly deleted'})




