from django.test import TestCase
import os

# Create your tests here.

def add_nfs_share(foldername , vgname , filesystemname , host):
    folderpath = f'/NfsShares/{foldername}'
    os.system('cp /etc/expots /project/nfsproject/exportsbackup')
    if os.system(f'mkdir -p {folderpath}') == 0:
        if os.system(f'chmod 770 {folderpath}') == 0:
            if os.system(f'mount {filesystemname} {folderpath}') == 0:
                if os.system(f'echo "{folderpath} {host}(rw,sync,no_subtree_check)" >> /etc/exports'):
                    if os.system('exportfs -a') == 0:
                        if os.system('systemctl restart nfs-kernel-server') == 0:
                            if os.system(f'ufw allow from {host} to any port nfs') == 0:
                                if os.system('ufw enable') == 0:
                                    print('okkkk')
    
    






















add_nfs_share()