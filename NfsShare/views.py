import json , os
from django.shortcuts import render , HttpResponse
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
    responsedict = dict()
    nfsnumber = 1
    for i in details:
        responsedict[f'NFS-{nfsnumber}'] = str(i.Name) +','+str(i.NasServer) +','+ str(i.filesystem_set.all()[0]) +','+ str(i.Host) +','+ str(i.mountPoint)

    return HttpResponse(status = 200)



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
                                        return HttpResponse(status = 201)
                                    addrolback(folderpath)
                                    return HttpResponse(status = 500)
                                addrolback(folderpath)
                                return HttpResponse(status = 500)
                            addrolback(folderpath)
                            return HttpResponse(status = 500)
                        addrolback(folderpath)
                        return HttpResponse(status = 500)
                    os.system(f'umount {folderpath}')
                    os.system(f'rm -r {folderpath}')
                    return HttpResponse(status = 500)
                os.system(f'rm -r {folderpath}')
                return HttpResponse(status = 500)
            os.system(f'rm -r {folderpath}')
            return HttpResponse(status = 500)
        #print(folderName + poolName + fileSystemName + host)
        return HttpResponse(status = 500)
    
    
    #check pool  ''
    pool_filesystem = VolumeGroup.objects.all()
    if pool_filesystem.count() == 0:
        return HttpResponse("<p>you dont have any pool pleas create a pool and file system first</p>")
    
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
        return  HttpResponse("<p>you dont have any filesystem pleas create file system first</p>")   

    #check Host   you dont have any host pleas create host
    if Host.objects.all().count() == 0:
        return  HttpResponse("<p>you dont have any host pleas create host</p>")



    return HttpResponse(status = 200)





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
    return HttpResponse(status = 200)




