import json , os
from django.shortcuts import render , HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pool.models import VolumeGroup
from pool.views import validating_name
from FileSystem.models import FileSystem
from Host.models import Host
from .models import NfsShare

# Create your views here.

def addrolback(nfspath):
    os.system(f'umount {nfspath}')
    os.system('cp  /project/nfsproject/exportsbackup  /etc/exports')
    os.system(f'rm -r {nfspath}')
    os.system('exportfs -a')
    os.system('systemctl restart nfs-kernel-srver')

#functions used in views ^    
#---------------------------------------------details-----------------------------------------------#
@csrf_exempt
def full_details(request):
    #add
    if request.method == 'POST':
        #check pool
        if have_filesystem() == 2:
            return  HttpResponse("<p>you don't have any pool pleas create a pool and file system first</p>")
        elif have_host() != 0 :
            return  HttpResponse("<p>you don't have any host pleas create host</p>")
        
        folderName  = request.POST.get('folderName')
        if validating_name(folderName) == False :
            return HttpResponse(f'<p>{folderName} is incorrect</p>')
        elif  NfsShare.objects.filter(Name = folderName).count() != 0:
            return HttpResponse(f'<p>{folderName} is alredy used</p>')
        
        fileSystemName = request.POST.get('fileSystem')
        if validating_name(fileSystemName) == False :
            return HttpResponse(f'<p>{fileSystemName} is incorrect</p>')
        
        host = request.POST.get('host')
        server = request.POST.get('server') 


        fileSystemPath = FileSystem.objects.get(fileSystemName = fileSystemName).lvpath
        hostIp = Host.objects.get(Name = host).IpAddress
        return create_nfs_share(folderName , fileSystemPath , hostIp , server , fileSystemName , host)
    # end add
    
 
    details = NfsShare.objects.all()
    responsedict = dict()
    nfsnumber = 1
    for i in details:
        responsedict[f'NFS-{nfsnumber}'] = str(i.Name) +','+str(i.NasServer) +','+ str(i.filesystem_set.all()[0]) +','+ str(i.Host) +','+ str(i.mountPoint)

    return HttpResponse(json.dumps(responsedict))




#---------------------------------------------remove-------------------------------------------------#
@csrf_exempt
def specifies_details(request , nfsname):
    if request.method == 'DELETE':
        if validating_name(nfsname) == False :
            return HttpResponse(f'<p>{nfsname} is incorrect</p>')
        try:
            nfspath = f'/NfsShares/{nfsname}'
            os.system(f'umount {nfspath}')
            os.system(f"sed -i '/{nfsname}/d' /etc/exports")
            os.system(f'rm -r {nfspath}')
            os.system('exportfs -a')
            os.system('systemctl restart nfs-kernel-server')
            db = NfsShare.objects.get(Name = nfsname)
            db.delete()
            return HttpResponse(f"<p>{nfsname} successfuly removed </p>",status = 200)
        except:
            return HttpResponse(f"<p>{nfsname} does not exist </p>")


    return HttpResponse(status = 200)






#------------------------------------------------------------------------------------#

def create_nfs_share(folderName , fileSystemPath , hostIp , server, fileSystemName , hostname):
    folderpath = f'/NfsShares/{folderName}'
    os.system('cp /etc/exports /project/nfsproject/exportsbackup')
    if os.system(f'mkdir -p {folderpath}') == 0:
        if os.system(f'chmod 770 {folderpath}') == 0:
            if os.system(f'mount {fileSystemPath} {folderpath}') == 0:
                if os.system(f'echo "{folderpath} {hostIp}(rw,sync,no_subtree_check)" >> /etc/exports') == 0:
                    if os.system('exportfs -a') == 0:
                        if os.system('systemctl restart nfs-kernel-server') == 0:
                            if os.system(f'ufw allow from {hostIp} to any port nfs') == 0:
                                if os.system('ufw enable') == 0:
                                    db = NfsShare(Name = folderName , mountPoint = folderpath ,NasServer = server ,Host = Host.objects.get(Name = hostname))
                                    db.save()
                                    FileSystem.objects.get(fileSystemName = fileSystemName).NfsShare.add(db)

                                    return HttpResponse("<p>Nfs share successfuly created</p>",status = 201)
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




def have_filesystem():
    Response = dict()
    for pool in VolumeGroup.objects.all():
        temproryList = list()
        for filesystem in  pool.FileSystem.distinct():
            temproryList.append(str(filesystem))
        if  ','.join(temproryList) == '':
            continue
        Response[pool.VgName] = ','.join(temproryList)

    if Response == {}:
        return  2
    return Response

def have_host():
    if Host.objects.all().count() == 0:
        return  2
    return 0        
 
