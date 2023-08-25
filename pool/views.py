from django.shortcuts import render , HttpResponse , get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import subprocess , shlex , os , re , json
from .models import VolumeGroup

# Create your views here.
def vgs():
    return str(subprocess.Popen('vgs' , stdout=subprocess.PIPE , shell=True).communicate()[0]).split('\\n')

#---------------------------------------------details--------------------------------------------#
@csrf_exempt
def full_details(request):
    # add pool
    if request.method == 'POST':
        vgname = request.POST.get('vgname')
        if validating_name(vgname) == False :
            return HttpResponse(f"<p>{vgname} is incorrect</p>")
        # start find available_disk_list 
        available_disk_list  = available_disk()
        #end finding available_disk_list 
        if available_disk_list == None :
            return HttpResponse("<p>you dont have a disk</p>")

        i = 0
        while i < len(available_disk_list):
            pvcreate = os.system(f'pvcreate {available_disk_list[i]}')
            if i == len(available_disk_list)-1 and pvcreate != 0:
                return HttpResponse("<p>you dont have a usable disk</p>")
            elif pvcreate == 0:
                if os.system(f'vgcreate {vgname} {available_disk_list[i]}') == 0:
                    db = VolumeGroup(PvPath = available_disk_list[i] , VgName = vgname)
                    db.save()
                    return HttpResponse("<p>pool successfuly created</p>")
                os.system(f'pvremove {available_disk_list[i]}')
                return HttpResponse("<p>name error</p>")
            i+=1
        
    # end add 
    
    allDetails  = vgs()
    allDetails.pop()
     
    if len(allDetails) == 0:
        res = {'msg':"you don't have any pool"}
        res = json.dumps(res)
        return HttpResponse(res     )
    allDetails.remove(allDetails[0])
    responsedict = dict()
    flag = 1
    for vgindex in range(len(allDetails)):
        responsedict[f'vg-{flag}'] = allDetails[vgindex]
        flag += 1


    responsedict = json.dumps(responsedict)
    

    return HttpResponse(responsedict)



#---------------------------------------------remove-------------------------------------------#   
@csrf_exempt
def specifies_details(request , **kwargs):
        if request.method == 'DELETE':
            vgname = kwargs['vgname']
            

            if validating_name(vgname) == False:
                return HttpResponse(f'{vgname} is incorrect ')
            query = get_object_or_404(VolumeGroup , VgName = vgname)
            pvpath = query.PvPath
            if query.FileSystem.all().count() != 0:
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
    

#----------------------------------------------------------------------------------#
def validating_name(name):
    if name[0]=='_' or name[0].isnumeric():
        return False
    elif '#' in name or ',' in name or '.' in name or '-' in name:
        return False
    return True

def available_disk():
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
    if len(available) <= 0:
        return None
        
    return available
