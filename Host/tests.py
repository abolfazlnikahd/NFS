#from django.test import TestCase
import subprocess
# Create your tests here.

dt = str(subprocess.Popen('ping -c 1 192.168.1.2' , stdout=subprocess.PIPE , shell=True).communicate())
if '0% packet loss' in dt :
    print('access')