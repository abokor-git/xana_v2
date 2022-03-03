from django_extensions.management.jobs import QuarterHourlyJob

from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from apps.app.models import AlertConfig

class Job(QuarterHourlyJob):
    help = "Topup Services Status !"

    def execute(self):
        
        host = "10.39.230.58"
        port = 22
        username = "topup"
        password = "topup"

        command = "/home/topup/jdk1.8.0_66/bin/jps"

        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(host, port, username, password)

        stdin, stdout, stderr = ssh.exec_command(command)
        lines = stdout.readlines()

        ssh.close()

        Jps = False
        Topup = False
        Bootstrap = False

        for x in lines:

            if x.find('Jps'):
                Jps = True

            if x.find('Top_Up_Djib.jar'):
                Topup = True

            if x.find('Bootstrap'):
                Bootstrap = True

        if Jps==True:
            AlertConfig.objects.filter(params='topup_jps').update(values="OK")
        else:
            AlertConfig.objects.filter(params='topup_jps').update(values="KO")

        if Topup==True:
            AlertConfig.objects.filter(params='topup_jar').update(values="OK")
        else:
            AlertConfig.objects.filter(params='topup_jar').update(values="KO")

        if Bootstrap==True:
            AlertConfig.objects.filter(params='topup_bootstrap').update(values="OK")
        else:
            AlertConfig.objects.filter(params='topup_bootstrap').update(values="KO")

        ##################################################################################

        if Jps==False or Topup==False or Bootstrap==False:

            """ Variable email """
            # Set Global Variables
            gmail_user = 'abokor.ahmed.kadar.nour@gmail.com'
            gmail_password = 'Mail.gmail.abokor'
            # Create Email 
            mail_from = 'Abokor Ahmed-Kadar Nour'
            #mail_to = 'abdoulkader_osman@intnet.dj,abdillahi_sougueh@intnet.dj,ismael.mourad@intnet.dj,nagwa_issam@intnet.dj,mouna_zain@intnet.dj,abdek.housssein@gmail.com,dt.bss.abdifatah@gmail.com,miwsaban@gmail.com,abokor.ahmed.kadar@outlook.com'
            mail_to = 'ismael.mourad@intnet.dj,nagwa_issam@intnet.dj,mouna_zain@intnet.dj,abdek.housssein@gmail.com,dt.bss.abdifatah@gmail.com,miwsaban@gmail.com,abokor.ahmed.kadar@outlook.com'
            mail_subject = 'Monitoring System !'

            message = MIMEMultipart('alternative')
            message['Subject'] = mail_subject
            message['From'] = mail_from
            message['To'] = mail_to

            mail_message_body = '''\
            Hi,

            Veuillez savoir que la plateforme de monitoring du TOPUP détecte des services down .
            
            Jps : %s
            Top_up_jar : %s
            Bootstrap : %s

            Interface Web : 172.16.1.89

            Cordialement,

            Xana System
            ''' % (Jps, Topup, Bootstrap)

            message.attach(MIMEText(mail_message_body, 'plain'))
            # Sent Email
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(gmail_user, gmail_password)
            server.sendmail(mail_from,mail_to.split(","), message.as_string())
            server.close()

        pass