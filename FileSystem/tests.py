#from django.test import TestCase
import subprocess
# Create your tests here.

all = str(subprocess.Popen('lsblk -f' , stdout=subprocess.PIPE , shell=True).communicate()[0]).split('\\n')
for i in all:
    if 'LVM' in i:
        print(i)

print('----------------')
print(all)
x = """ """
