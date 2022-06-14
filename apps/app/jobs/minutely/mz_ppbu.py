import gzip
from django_extensions.management.jobs import MinutelyJob

from datetime import datetime, timedelta
import pandas as pd

from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient

from apps.app.models import FilePPBU, DataPPBU

class Job(MinutelyJob):
    help = "My sample job."

    def execute(self):

        """ La date et l'heure """
        datetime_today = datetime.now()
        date_today = datetime_today.strftime("%Y-%m-%d %H:%M:%S")
        
        host = "10.39.230.61"
        port = 22
        username = "mzapp"
        password = "MZ.user2020"

        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(host, port, username, password)

        command = "cd /MZ_DATA/archive/SW-OCS_NON_VOICE/ && ls 2022-*/ocsstd_PPBU*"
        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()
        """print(lines)"""
        
        folder = []
        files = []

        for x in lines:
            
            itemFilePPBU = FilePPBU.objects.filter(file=x[11:],folder=x[0:10]).exists()
            if itemFilePPBU == False:

                folder.append(x[0:10])
                files.append(x[11:])
                FilePPBU.objects.create(file=x[11:],folder=x[0:10],created_date=date_today)

        """for x in range(len(folder)):
            print("folder : "+folder[x]+" file : "+files[x])"""

        # SCPCLient takes a paramiko transport as an argument
        scp = SCPClient(ssh.get_transport())
        # upload it directly from memory
        
        for x in range(len(files)):
            file = '/MZ_DATA/archive/SW-OCS_NON_VOICE/'+str(folder[x])+'/'+str(files[x].strip())
            scp.get(file,local_path='./tmp/')

        # close connection
        scp.close()

        ssh.close()

        for x in range(len(files)):

            itemFilePPBU = FilePPBU.objects.get(file=files[x],folder=folder[x])
            #print(itemFilePPBU.id)

            file = './tmp/'+str(files[x].strip())
            #print(file)

            with gzip.open(file, 'rb') as f:
                file_content = f.read()

            all_cdr_in_file = file_content.decode('UTF-8')

            list_of_cdr = list(all_cdr_in_file.split("\n"))
            
            for y in list_of_cdr:
                
                if y!='':
                    #print('###############################')
                    #print(y)
                    cdr_detail = list(y.split(" "))
                    date_r = str(cdr_detail[6][0:4])+"-"+str(cdr_detail[6][4:6])+"-"+str(cdr_detail[6][6:8])+" "+str(cdr_detail[6][8:10])+":"+str(cdr_detail[6][10:12])+":"+str(cdr_detail[6][12:14])
                    DataPPBU.objects.create(numero=cdr_detail[11],date_recharge=date_r,profil_ocs=cdr_detail[32],data=y,id_fileppbu_id=itemFilePPBU.id)
                    #print("Numéro : "+cdr_detail[11]+" DR : "+date_r+" Profil : "+cdr_detail[32])
                    #print('###############################')
        
        pass
