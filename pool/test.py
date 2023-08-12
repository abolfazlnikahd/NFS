import subprocess , shlex , re , json

"""
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
def vgs():
    return str(subprocess.Popen('vgs' , stdout=subprocess.PIPE , shell=True).communicate()[0]).split('\\n')
def lvs():
    return str(subprocess.Popen('lvs' , stdout=subprocess.PIPE , shell=True).communicate()[0]).split('\\n')
""" 
 """

def an():
    allDetails = vgs()
    allDetails.pop()
    lenall = len(allDetails)
    if lenall == 0:
        return 1
    allDetails.remove(allDetails[0])
    for index in range(lenall -1 ):
        temporarylist = list()
        #print(index)
        allDetails[index] = allDetails[index].strip().split(' ')
        for ob in range(len(allDetails[index])):
            if allDetails[index][ob] != '':
                #print(allDetails[index][ob])
                temporarylist.append(allDetails[index][ob])
        #allDetails[index].clear()
        allDetails[index] = temporarylist.copy()

    vgnum = 0
    frontdict = 0
    
    print((allDetails))

an()


"""

volumegs = vgs()
volumegs.pop()
if len(volumegs) > 0:
    rlvgs = range(len(volumegs))
    volumegs.remove(volumegs[0])

    for index in rlvgs:
        temporaryVolumeGroupList = list()
        volumegs[index] = str(volumegs[index]).strip().split(' ')
        for i in range(len(volumegs[index])):
            if volumegs[index][i] != '':
                temporaryVolumeGroupList.append(volumegs[index][i])
        volumegs[index].clear()
        volumegs[index] = temporaryVolumeGroupList.copy()
        volumegs[index].append([])
        volumegs[index].append([])
print(volumegs)
    
    
    physycalvs = pvs()
    physycalvs.pop()
    physycalvs.remove(physycalvs[0])
    for pindex in range(len(physycalvs)):
        temporaryPhysycalVolumeList = list()
        physycalvs[pindex] = str(physycalvs[pindex]).split(' ')
        for p in range(len(physycalvs[pindex])):
            if physycalvs[pindex][p] != '':
                temporaryPhysycalVolumeList.append(physycalvs[pindex][p])
        physycalvs[pindex].clear()
        physycalvs[pindex] = temporaryPhysycalVolumeList.copy()
    
    logicalvs = lvs()
    logicalvs.pop()
    if len(logicalvs) > 0:
        logicalvs.remove(logicalvs[0])

        for lvindex in range(len(logicalvs)):
            temporaryLogicalVolumeList = list()
            logicalvs[lvindex] = str(logicalvs[lvindex]).split(' ')
            for l in range(len(logicalvs[lvindex])):
                if logicalvs[lvindex][l] != '':
                    temporaryLogicalVolumeList.append(logicalvs[lvindex][l])
            logicalvs[lvindex].clear()
            logicalvs[lvindex] = temporaryLogicalVolumeList.copy()
    



#print(volumegs)
#print(physycalvs)
#print(logicalvs)

        


 {vgname:name , pvnumber:int , pvpath:list , lvnumber:int , lvnames:list names , vsize:int , vfree:int } """


