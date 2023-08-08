import subprocess , shlex , re


def addpool():
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
    print(available)


def pooldetails():
    all  = str(subprocess.Popen('vgs' , stdout=subprocess.PIPE , shell=True).communicate()[0]).split('\\n')
    all.pop()
    if len(all) == 0:
        print('nook')
        return 0
    all.remove(all[0])
    print(all)


#pooldetails()
def vgs():
    return str(subprocess.Popen('vgs' , stdout=subprocess.PIPE , shell=True).communicate()[0]).split('\\n')
""" 

allVolumeGroupDetails = vgs()
allVolumeGroupDetails.pop()
#print(allVolumeGroupDetails)
allVolumeGroupDetails.remove(allVolumeGroupDetails[0])
VGnames = dict()
for details in allVolumeGroupDetails:
    splitedListOfDetails = str(details).strip().split(' ')
    VGnames[splitedListOfDetails[0]] = int(splitedListOfDetails[6])
    
print(VGnames)
 """
def pvs():
    return str(subprocess.Popen('pvs' , stdout=subprocess.PIPE , shell=True).communicate()[0]).split('\\n')

physycalVolumesDetails = pvs()
physycalVolumesDetails.pop()
