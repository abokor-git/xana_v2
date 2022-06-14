from django_extensions.management.jobs import BaseJob

import subprocess as sp

from notify_run import Notify

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Job(BaseJob):
    help = "My sample job."

    def execute(self):
        
        ip = "10.39.231.23"
        status,result = sp.getstatusoutput("ping -c 2 " + ip)

        if status == 0: 
            
            print("System " + ip + " is UP !")
        
        else:

            #link = "http://172.32.1.45:8190/#/"

            #""" Variable email """
            # Set Global Variables
            #gmail_user = 'xana.system.v2@outlook.com'
            #gmail_password = 'Xana_v2_system'
            # Create Email 
            #mail_from = 'Xana System'
            #mail_to = 'nagwa_issam@intnet.dj,mouna_zain@intnet.dj,abdek.housssein@gmail.com,dt.bss.abdifatah@gmail.com,abokor.ahmed.kadar@outlook.com'
            #mail_to = 'abokor.ahmed.kadar@outlook.com, abokor.ahmed.kadar.nour@gmail.com'
            #mail_subject = 'VPN PROBLEM !!!'

            #mail_message_body = """\
            #<html>
            #<head></head>
            #<body>
            #    <p>Bonjour/Bonsoir,<br><br>
            #    Veuillez reactivez le Vpn svp :<br><br>
            #    Vous trouverez plus de détails <a href="%s">ici</a><br><br>
            #    Cordialement,<br><br>
            #    XANA SYSTEM
            #    </p>
            #</body>
            #</html>
            #""" % (link)

            #message = MIMEMultipart('alternative')
            #message['Subject'] = mail_subject
            #message['From'] = mail_from
            #message['To'] = mail_to
            
            #message.attach(MIMEText(mail_message_body, 'html'))

            # Sent Email
            #server = smtplib.SMTP('smtp-mail.outlook.com', 587)
            #server.starttls()
            #server.login(gmail_user, gmail_password)
            #server.sendmail("xana.system.v2@outlook.com",mail_to.split(","),msg=message.as_string())
            #server.close()

            notify = Notify()
            notify.send("VPN desactiver !!!")

        pass

